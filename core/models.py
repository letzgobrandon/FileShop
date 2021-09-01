from django.db import models
import uuid
from uuid import UUID
from typing import Optional, Dict
from .constants import CURRENCY_CHOICES
from django.utils.crypto import get_random_string
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.


class Product(models.Model):
    token: UUID = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=False
    )  # token to withdraw
    uid: UUID = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=False
    )  # public identifier
    product_name: Optional[str] = models.CharField(
        max_length=255, blank=True, null=True
    )
    product_description: Optional[str] = models.TextField(max_length=1023, null=True)
    secret_description: Optional[str] = models.TextField(max_length=1023, null=True)
    price: float = models.FloatField(default=0)
    currency: str = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default="USD"
    )
    email: Optional[str] = models.EmailField(null=True)
    hit_count_generic: HitCount = GenericRelation(
        HitCount,
        object_id_field="object_pk",
        related_query_name="hit_count_generic_relation",
    )

    def __str__(self):
        return "Product " + str(self.product_name)

    @property
    def btc_balance(self) -> float:
        pay_dict: Optional[Dict] = self.orders.filter(
            crypto="BTC", status_of_transaction=2
        ).aggregate(models.Sum("received_value"))
        if pay_dict["received_value__sum"] is not None:
            return pay_dict["received_value__sum"]
        return 00.00

    @property
    def bch_balance(self) -> float:
        pay_dict: Optional[Dict] = self.orders.filter(
            crypto="BCH", status_of_transaction=2
        ).aggregate(models.Sum("received_value"))
        if pay_dict["received_value__sum"] is not None:
            return pay_dict["received_value__sum"]
        return 00.00

    def update_email(self, email):
        self.email = email
        self.save(update_fields=['email', ])
    
    @property
    def files(self):
        return File.objects.filter(product=self)

class File(models.Model):
    product: Product = models.ForeignKey(
        Product, related_name="files", on_delete=models.CASCADE
    )
    uid: UUID = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=False)
    file_data = models.BinaryField()
    file_name: Optional[str] = models.TextField(null=True)


class Order(models.Model):
    class StatusChoices(models.IntegerChoices):
        NOT_STARTED = -1
        UNCONFIRMED = 0
        PARTIAL_CONFIRMED = 1
        CONFIMED = 2

    class CryptioChoices(models.TextChoices):
        BTC = "BTC"
        BCH = "BCH"

    uid: UUID = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=False)
    status_of_transaction: int = models.IntegerField(
        choices=StatusChoices.choices, default=StatusChoices.NOT_STARTED
    )
    expected_value: Optional[float] = models.DecimalField(
        null=True, decimal_places=10, max_digits=100
    )
    usd_price: Optional[float] = models.DecimalField(
        null=True, decimal_places=10, max_digits=100
    )
    received_value: Optional[float] = models.DecimalField(
        blank=True, null=True, decimal_places=10, max_digits=100
    )
    txid: Optional[str] = models.TextField(null=True)
    address: str = models.TextField(null=True, unique=True)
    product: Product = models.ForeignKey(
        Product, related_name="orders", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now=True)
    crypto = models.CharField(max_length=255, choices=CryptioChoices.choices, null=True)
