from django.conf import settings
from django.shortcuts import get_object_or_404, reverse
from django.core.validators import validate_email
from django.core.exceptions import PermissionDenied, ValidationError
from requests.api import request

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException

from .models import Product, File, Order
from .constants import SUPPORTED_CRYPTOS, SUPPORTED_CURRENCIES
from .serializers import ProductSerializer, OrderSerializer, ProductSensitiveSerializer
from .utils import email_helper, create_order_helper
from .blockonomics_utils import exchanged_rate

class AnonymousView(APIView):

    permission_classes = [AllowAny, ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_exception_handler(self):
        default_handler = super().get_exception_handler()

        def handle_exception(exc, context):
            if not isinstance(exc, self.BaseException):
                return default_handler(exc, context)
            
            is_handled = False
            response_payload = {}
            
            if isinstance(exc, self.MissingParametersError):
                is_handled = True

                if hasattr(exc, 'error_fields'):
                    response_payload['error'] = {}
                    for e in exc.error_fields:
                        response_payload['error'][e] = ["This field is required!", ]
                
            elif isinstance(exc, self.UnsupportedCryptoError):
                is_handled = True
            elif isinstance(exc, self.UnsupportedCurrencyError):
                is_handled = True
            
            if is_handled:
                if hasattr(exc, 'error_key'):
                    if not response_payload.get('error'):
                        response_payload['error'] = {}
                    response_payload['error'][exc.error_key] = exc.default_detail
                else:
                    response_payload['error_msg'] = exc.default_detail
                    response_payload['error_code'] = exc.default_code
                
                return Response(
                    data = response_payload,
                    status = exc.status_code
                )
            else:
                return default_handler(exc, context)
        
        return handle_exception
    
    def check_supported_currency(self, currency, raise_error=True):

        if not currency:
            if raise_error:
                raise self.MissingParametersError(fields=['currency', ])
            return False

        if str(currency).upper() not in SUPPORTED_CURRENCIES:
            if raise_error:
                raise self.UnsupportedCurrencyError()
            return False
            
    def check_supported_crypto(self, currency, raise_error=True):

        if not currency:
            if raise_error:
                raise self.MissingParametersError(fields=['crypto', ])
            return False

        if str(currency).upper() not in SUPPORTED_CRYPTOS:
            if raise_error:
                raise self.UnsupportedCurrencyError()
            return False

    class BaseException(APIException):
        def __init__(self, fields=None, *args, **kwargs):
            self.error_fields = fields
            super().__init__(*args, **kwargs)

    class MissingParametersError(BaseException):
        status_code = 400
        default_detail = 'Missing Parameters'
        default_code = 'ERR_MISSING_PARAMETERS'

    class UnsupportedCurrencyError(BaseException):
        status_code = 400
        default_detail = 'This currency is not supported yet'
        default_code = 'ERR_UNSUPPORTED_CURRENCY'
        error_key = 'currency'
    
    class UnsupportedCryptoError(BaseException):
        status_code = 400
        default_detail = 'This crypto is not supported yet'
        default_code = 'ERR_UNSUPPORTED_CRYPTO'
        error_key = 'crypto'

class ProductCreateAPIView(AnonymousView, generics.CreateAPIView):
    model = Product
    serializer_class = ProductSerializer

    def create(self, *args, **kwargs):
        
        files = self.request.FILES.getlist('files')

        if not files:
            return Response({
                "error": {
                    "files": ["Atleast 1 File is required!"]
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=self.request.data)
        if not serializer.is_valid():
            return Response({
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        product = serializer.save()

        for _file in files:
            File.objects.create(
                product=product, file_data=_file.file.read(), file_name=_file.name
            )

        # self.request.session["product_id"] = product.pk # To be removed

        data = {
            "uuid": product.uid,
            "token": product.token
        }

        return Response(data=data, status=status.HTTP_201_CREATED)

class ProductAPIView(generics.RetrieveAPIView, generics.UpdateAPIView):

    model = Product
    queryset = model.objects.all()
    email_template = "emails/product_page.html"

    def get_serializer_class(self):
        if (self.request.method == 'GET' and self.request.query_params.get('token') != None) or \
           (self.request.method != 'GET' and self.request.data.get('token') != None) :
            return ProductSensitiveSerializer
        
        return ProductSerializer

    def get_object(self, *args, **kwargs):
        query = {
            "uid": self.kwargs.get("uid")
        }

        if self.request.method != 'GET':
            token = self.request.data.get('token')
            if not token:
                raise PermissionDenied({"token": "Token is required to perform this operation"})
            
            query['token'] = token
        
        try:
            return self.get_queryset(*args, **kwargs).get(**query)
        except self.model.DoesNotExist:
            raise NotFound("Product not found")
        
    def check_email(self):
        """Check if Email was in payload, then trigger the Email
        
        This Method does not check for Response Status and it must be checked 
        for a success status (20X) before calling this method.

        """
        if not self.request.data.get('email'):
            return

        product = self.get_object()

        track_uri = self.request.build_absolute_uri(
            reverse("core:product_info_seller", kwargs={"token": product.token})
        )

        extra_email_context = {
            "track_uri": track_uri,
            "public_uri": self.request.build_absolute_uri(
                reverse("core:product_info_buyer", kwargs={"uid": product.uid})
            )
        }

        email_helper(
            self.request,
            product.email,
            self.email_subject,
            self.email_template,
            html_email_template_name=self.email_template,
            extra_email_context=extra_email_context,
        )
    
    def update(self, *args, **kwargs):

        response = super().update(*args, **kwargs)
        if response.status_code == 200:
            self.check_email()
        
        return response

    def partial_update(self, *args, **kwargs):

        response = super().partial_update(*args, **kwargs)
        if response.status_code == 200:
            self.check_email()
        
        return response


# class CurrencyConverterAPIView(AnonymousView):

#     def post(self, *args, **kwargs):

#         currency = self.request.data.get('currency', 'USD')
#         price = self.request.data.get('price')
#         crypto = self.request.data.get('crypto')

#         self.check_supported_currency(currency)
#         self.check_supported_crypto(crypto)
        
#         if price == None:
#             raise self.MissingParametersError(fields=['price', ])

#         try:
#             price = float(price)
#         except ValueError:
#             return Response({
#                 "error": {
#                     "price": ["Must be a valid value.", ]
#                 }
#             }, status=status.HTTP_400_BAD_REQUEST)
        
#         bits = exchanged_rate(price, crypto, currency)
#         converted_price = bits/pow(10, 8)

#         return Response({
#             "bits": bits,
#             "price": converted_price
#         })

class InitiateProductBuyAPIView(AnonymousView):

    def post(self, *args, **kwargs):

        product_uid = self.request.data.get('product_uid')
        if not product_uid:
            raise self.MissingParametersError(fields=['product_uid', ])
        
        try:
            product = Product.objects.get(uid=product_uid)
        except self.model.DoesNotExist:
            raise NotFound("Product not found")

        crypto = self.request.data.get('crypto', 'BTC')
        self.check_supported_crypto(crypto)

        order: Order = create_order_helper(self.request, product, crypto, product.price)
        
        return Response({
            "order_uuid": order.uid,
        })

class OrderAPIView(AnonymousView, generics.RetrieveAPIView):

    model = Order
    serializer_class = OrderSerializer
    queryset = model.objects.all()

    def get_object(self):
        try:
            return self.get_queryset().get(uid=self.kwargs['uid'])
        except self.model.DoesNotExist:
            raise NotFound("Order Not Found")

class OrderConfirmCallbackAPIView(AnonymousView):

    def post(self, *args, **kwargs):
        
        status_of_transaction = self.request.data.get("status", None)
        if not status_of_transaction:
            raise self.MissingParametersError(fields=['status_of_transaction', ])

        order = get_object_or_404(Order, uid=kwargs['uid'])

        if status_of_transaction >= order.status_of_transaction:
            order.status_of_transaction = max(
                order.status_of_transaction, status_of_transaction
            )
            order.save()

            return Response()

        return Response({
            "error": {
                "status": ["Order status wasn't changed.", ]
            }
        }, status=status.HTTP_400_BAD_REQUEST)

class OrderCallbackView(AnonymousView):

    def get(self, *args, **kwargs):

        secret = settings.CALLBACK_SECRET

        secret_from_request = self.request.query_params.get('secret')

        if secret != secret_from_request:
            raise PermissionDenied("Invalid Request")
        
        txid = self.request.query_params.get('txid')
        value = self.request.query_params.get('value')
        status = int(self.request.query_params.get('status', -1))
        addr = self.request.query_params.get('addr')

        try:
            order = Order.objects.get(address=addr)
        except Order.DoesNotExist:
            raise PermissionDenied("Invalid Address")

        print(status)
        
        if status >= order.status_of_transaction:
            order.status_of_transaction = max(
                order.status_of_transaction, status
            )
            order.received_value = value
            order.txid = txid
            order.save()

            return Response()

        return PermissionDenied("Status cannot be updated at this stage")
    