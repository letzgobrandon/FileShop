from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Product, File, Order, Withdrawl


class FileSerializer(serializers.ModelSerializer):

    file_size = SerializerMethodField()

    class Meta:
        model = File
        fields = ['uid', 'file_name', 'file_size']

    def get_file_size(self, obj: File):
        return len(obj.file_data)

class ProductSerializer(serializers.ModelSerializer):

    num_files = SerializerMethodField()
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "currency", "price", "product_name", 
            "product_description", "num_files", "files"
        ]

    def get_num_files(self, obj: Product):
        return obj.files.count()

class ProductSensitiveSerializer(serializers.ModelSerializer):

    num_files = SerializerMethodField()
    hits = SerializerMethodField()
    files = FileSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "uid", "token", "email",
            "currency", "price", "product_name", 
            "product_description", "num_files", "files",
            "hits"
        ]

    def get_num_files(self, obj: Product):
        return obj.files.count()
    
    def get_hits(self, obj: Product):
        return obj.hit_count.hits

class OrderSerializer(serializers.ModelSerializer):

    product_uid = SerializerMethodField()
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "uid", "status_of_transaction", "expected_value", 
            "usd_price", "received_value", "address", "crypto", 
            "timestamp", "product_uid", "product", "is_payment_complete"
        ]

    def get_product_uid(self, obj):
        return obj.product.uid

class OrderSensitiveSerializer(serializers.ModelSerializer):

    product_uid = SerializerMethodField()
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def get_product_uid(self, obj):
        return obj.product.uid
    
class WithdrawlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Withdrawl
        fields = [
            'uid', 'created_on', 'modified_on',
            'address', 'txid', 'amount', 'status',
            'crypto'
        ]
    