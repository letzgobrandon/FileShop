from django.shortcuts import get_object_or_404, reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import Product, File
from .serializers import ProductSerializer
from .utils import email_helper, create_payment_helper
from .blockonomics_utils import exchanged_rate

class ProductCreateAPIView(generics.CreateAPIView):
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

        self.request.session["product_id"] = product.pk

        data = {
            "data": serializer.data,
            "redirect_url": reverse("core:product_seller_email_updates")
        }

        return Response(data=data, status=status.HTTP_201_CREATED)

class EmailUpdateAPIView(APIView):

    email_template = "emails/product_page.html"

    def get_object(self):
        return get_object_or_404(
            Product, pk=self.request.session.get("product_id", None)
        )

    def post(self, *args, **kwargs):
        product = self.get_object()

        email = self.request.data.get('email')
        if not email:
            return Response({
                "error": {
                    "email": ["This field is required.", ]
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_email(email)
        except ValidationError:
            return Response({
                "error": {
                    "email": ["Please provide a valid email address.", ]
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        product.update_email(email)

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

        data = {
            "redirect_url": reverse("core:product_info_seller", kwargs={"token": product.token})
        }
        
        return Response(data=data)

class ProductPublicAPIView(generics.RetrieveAPIView):
    model = Product
    serializer_class = ProductSerializer
    queryset = model.objects.all()

    def get_object(self, *args, **kwargs):
        try:
            return self.get_queryset(*args, **kwargs).get(uid=self.kwargs.get("uid"))
        except self.model.DoesNotExist:
            raise NotFound("Product not found")

class CurrencyConverterAPIView(APIView):

    def post(self, *args, **kwargs):

        currency = self.request.data.get('currency', 'USD')
        price = self.request.data.get('price')
        crypto = self.request.data.get('crypto')

        if not currency:
            return Response({
                "error": {
                    "currency": ["This field is requried.", ]
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        supported_currencies = ['USD', ]
        if str(currency).upper() not in supported_currencies:
            return Response({
                "error": {
                    "currency": ["This currency is not yet supported.", ]
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if price == None:
            return Response({
                "error": {
                    "price": ["This field is requried.", ]
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            price = float(price)
        except ValueError:
            return Response({
                "error": {
                    "price": ["Must be a valid value.", ]
                }
            }, status=status.HTTP_400_BAD_REQUEST)



        if not crypto:
            return Response({
                "error": {
                    "crypto": ["This field is requried.", ]
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        supported_cryptos = ["BTC", ]
        if str(crypto).upper() not in supported_cryptos:
            return Response({
                "error": {
                    "crypto": ["This crypto is not yet supported.", ]
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        bits = exchanged_rate(price, crypto, currency)
        converted_price = bits/pow(10, 8)

        return Response({
            "bits": bits,
            "price": converted_price
        })

class InitiateProductBuyAPIView(APIView):

    def get_object(self, *args, **kwargs):
        try:
            return Product.objects.get(uid=self.kwargs.get("uid"))
        except self.model.DoesNotExist:
            raise NotFound("Product not found")

    def post(self, *args, **kwargs):
        
        crypto = self.request.data.get('crypto', 'BTC')
        supported_cryptos = ["BTC", ]
        if str(crypto).upper() not in supported_cryptos:
            return Response({
                "error": {
                    "crypto": ["This crypto is not yet supported.", ]
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        product = self.get_object()

        payment = create_payment_helper(self.request, product, crypto, product.price)
        
        return Response({
            "payment_url": "%s?crypto=%s" % (
                reverse('core:product_pay_buyer', kwargs={'order_id': payment.order_id}),
                crypto
            )
        })
