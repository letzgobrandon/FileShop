from django.shortcuts import reverse

from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product, File
from .serializers import ProductSerializer


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
    