from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Product, File, Order


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ['uid', 'file_name']

class ProductSerializer(serializers.ModelSerializer):

    num_files = SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "currency", "price", "product_name", 
            "product_description", "num_files"
        ]

    def get_num_files(self, obj: Product):
        return obj.files.count()

class ProductSensitiveSerializer(serializers.ModelSerializer):

    num_files = SerializerMethodField()
    files = FileSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "uid", "token", "email",
            "currency", "price", "product_name", 
            "product_description", "num_files", "files"
        ]

    def get_num_files(self, obj: Product):
        return obj.files.count()

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            "uid", "status_of_transaction", "expected_value", 
            "usd_price", "received_value", "address", "crypto", 
            "timestamp"
        ]
