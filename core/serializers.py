from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Product, File


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):

    num_files = SerializerMethodField()

    class Meta:
        model = Product
        fields = ["currency", "price", "product_name", "product_description", "num_files"]

    def get_num_files(self, obj: Product):
        return obj.files.count()
