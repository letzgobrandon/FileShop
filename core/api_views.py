import requests
from django.conf import settings
from django.shortcuts import reverse
from django.core.exceptions import PermissionDenied

from rest_framework import generics, status, filters
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException

from hitcount.models import HitCount
from hitcount.views import HitCountMixin

from .models import Product, File, Order, Withdrawl
from .constants import SUPPORTED_CRYPTOS, SUPPORTED_CURRENCIES
from .serializers import ProductSerializer, OrderSerializer, ProductSensitiveSerializer, WithdrawlSerializer, OrderSensitiveSerializer
from .utils import email_helper, create_order_helper
from .blockonomics_utils import BlockonomicsAPIError

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

class ProductAPIView(AnonymousView, generics.RetrieveAPIView, generics.UpdateAPIView, HitCountMixin):

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

        extra_email_context = {
            "track_uri": product.get_seller_dashboard_url(),
            "public_uri": product.get_public_url()
        }

        email_helper(
            self.request,
            product.email,
            self.email_subject,
            self.email_template,
            html_email_template_name=self.email_template,
            extra_email_context=extra_email_context,
        )

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if self.request.query_params.get('token') == None:
            instance: Product = self.get_object()
            hit_count = HitCount.objects.get_for_object(instance)
            self.hit_count(self.request, hit_count)

        return response
    
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

class ProductTokenMixin(object):

    def get_product(self) -> Product:
        try:
            return Product.objects.get(token=self.kwargs['token'])
        except Product.DoesNotExist:
            raise NotFound("Product not found")
    

class ProductOrdersListAPIView(AnonymousView, generics.ListAPIView, ProductTokenMixin):

    model = Order
    serializer_class = OrderSensitiveSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['timestamp', 'txid', 'uid']
    ordering = ['-timestamp', ]
    search_fields = ['txid', 'addr', 'uid']
    
    def get_queryset(self):
        product = self.get_product()
        return self.model.objects.filter(product=product)

class ProductBalancesAPIView(AnonymousView, ProductTokenMixin):

    def get(self, *args, **kwargs):

        product = self.get_product()

        data = {}

        for crypto in SUPPORTED_CRYPTOS:
            data[crypto.lower()] = product.get_balance(crypto)
        
        return Response(data)

class ProductWithdrawAPIView(AnonymousView, ProductTokenMixin):

    def post(self, *args, **kwargs):

        product = self.get_product()

        addr = self.request.data.get('address')
        crypto = self.request.data.get('crypto')

        if not addr:
            raise self.MissingParametersError(fields=['address', ])
        self.check_supported_crypto(crypto)
        crypto = crypto.upper()
        
        withdrawl: Withdrawl = product.request_withdrawl(crypto, addr)

        return Response({
            "uid": withdrawl.uid
        })

class ProductWithdrawlsListAPIView(AnonymousView, generics.ListAPIView, ProductTokenMixin):

    model = Withdrawl
    serializer_class = WithdrawlSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_on', 'modified_on', 'address', 'txid', 'uid']
    ordering = ['-created_on', ]
    search_fields = ['txid', 'address', 'uid']
    
    def get_queryset(self):
        product = self.get_product()
        return self.model.objects.filter(product=product)


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

        try:
            order: Order = create_order_helper(self.request, product, crypto, product.price)
        except (requests.HTTPError, BlockonomicsAPIError) as e:
            return Response({
                "error": {
                    "api": [str(e), ]
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
        
    
    # def patch(self, *args, **kwargs):

    #     serializer = self.get_serializer(data=self.request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response()


class OrderCallbackView(AnonymousView):

    email_template = "emails/payment.html"
    email_subject = "emails/product_page.txt"
    extra_email_context = {}

    def get(self, *args, **kwargs):

        secret = settings.CALLBACK_SECRET

        secret_from_request = self.request.query_params.get('secret')

        if secret != secret_from_request:
            raise PermissionDenied("Invalid Request")
        
        txid = self.request.query_params.get('txid')
        value = self.request.query_params.get('value', 0)
        status = int(self.request.query_params.get('status', -1))
        addr = self.request.query_params.get('addr')

        try:
            order: Order = Order.objects.get(address=addr)
        except Order.DoesNotExist:
            raise PermissionDenied("Invalid Address")

        if status >= order.status_of_transaction:
            order.status_of_transaction = max(
                order.status_of_transaction, status
            )
            order.received_value = float(value)/1e8
            order.txid = txid
            order.save()

            if order.status_of_transaction == order.StatusChoices.CONFIRMED:
                self.extra_email_context["track_uri"] = self.request.build_absolute_uri(
                    reverse(
                        "core:product_info_seller", kwargs={"token": order.product.token}
                    )
                )
                if order.product.email:
                    email_helper(
                        request,
                        order.product.email,
                        self.email_subject,
                        self.email_template,
                        html_email_template_name=self.email_template,
                        extra_email_context=self.extra_email_context,
                    )

            return Response()

        return PermissionDenied("Status cannot be updated at this stage")
    