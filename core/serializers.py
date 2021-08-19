from rest_framework import serializers

from .models import Product, File


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):

    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
