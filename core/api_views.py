from django.shortcuts import get_object_or_404, reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product, File
from .serializers import ProductSerializer
from .utils import email_helper

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

        # email_helper(
        #     self.request,
        #     product.email,
        #     self.email_subject,
        #     self.email_template,
        #     html_email_template_name=self.email_template,
        #     extra_email_context=extra_email_context,
        # )

        data = {
            "redirect_url": reverse("core:product_info_seller", kwargs={"token": product.token})
        }
        
        return Response(data=data)
    