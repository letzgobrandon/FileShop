from django.db import models
import uuid
from uuid import UUID
from typing import Optional, Dict
from .constants import CURRENCY_CHOICES
from django.utils.crypto import get_random_string
from hitcount.models import HitCount, HitCountMixin
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.


class Product(models.Model, HitCountMixin):
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
        return self.get_balance('BTC')

    @property
    def bch_balance(self) -> float:
        return self.get_balance('BCH')
    
    @property
    def product_files(self):
        return File.objects.filter(product=self)
    
    def get_balance(self, crypto) -> float:
        pay_dict: Optional[Dict] = self.orders.filter(
            crypto=crypto, status_of_transaction__gte=0
        ).aggregate(models.Sum("received_value"))

        balance = pay_dict["received_value__sum"]
        if balance is None:
            balance = 00.00

        withdrawl_dict: Optional[Dict] = self.withdrawls.filter(
            crypto=crypto, status=Withdrawl.StatusChoices.COMPLETED
        ).aggregate(models.Sum("amount"))

        withdrawl_balance = withdrawl_dict["amount__sum"]
        if withdrawl_balance is None:
            withdrawl_balance = 00.00
        
        return float(balance) - float(withdrawl_balance)
    
    def update_email(self, email):
        self.email = email
        self.save(update_fields=['email', ])
    
    def request_withdrawl(self, crypto: str, address: str):
        print(self.get_balance(crypto))
        return Withdrawl.objects.create(
            product=self,
            address=address,
            crypto=str(crypto).upper(),
            amount=self.get_balance(crypto)
        )

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
        CONFIRMED = 2

    class CryptioChoices(models.TextChoices):
        BTC = "BTC"
        BCH = "BCH"

    uid: UUID = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=False)
    status_of_transaction: int = models.IntegerField(
        choices=StatusChoices.choices, default=StatusChoices.NOT_STARTED
    )
    expected_value: Optional[float] = models.DecimalField(
        null=True, decimal_places=10, max_digits=65
    )
    usd_price: Optional[float] = models.DecimalField(
        null=True, decimal_places=10, max_digits=65
    )
    received_value: Optional[float] = models.DecimalField(
        blank=True, null=True, decimal_places=10, max_digits=65
    )
    txid: Optional[str] = models.TextField(null=True)
    address: str = models.TextField(null=True, unique=True)
    product: Product = models.ForeignKey(
        Product, related_name="orders", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now=True)
    crypto = models.CharField(max_length=255, choices=CryptioChoices.choices, null=True)

    is_payment_complete = models.BooleanField(default=False)
    # email = models.EmailField(null=True)

    def save(self, *args, **kwargs):
        self.check_payment_completion()
        super().save(*args, **kwargs)
    
    def check_payment_completion(self):
        if not self.received_value or not  self.expected_value:
            self.is_payment_complete = False
        else:
            if float(self.expected_value) <= float(self.received_value):
                self.is_payment_complete = True
            else:
                self.is_payment_complete = False

class Withdrawl(models.Model):

    class StatusChoices(models.TextChoices):
        PENDING = 'p'
        INITIATED = 'i'
        COMPLETED = 'c'
        REJECTED = 'r'

    class CryptoChoices(models.TextChoices):
        BTC = "BTC"
        BCH = "BCH"

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    uid: UUID = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=False)

    product: Product = models.ForeignKey(
        Product, related_name="withdrawls", on_delete=models.CASCADE
    )

    address: str = models.TextField()

    amount: float = models.DecimalField(
        decimal_places=10, max_digits=65
    )

    status: str = models.CharField(max_length=1, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    txid: Optional[str] = models.TextField(null=True)

    crypto = models.CharField(max_length=255, choices=CryptoChoices.choices, null=True)
