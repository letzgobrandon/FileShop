from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth.decorators import login_required

from .models import Order, Product, File, Withdrawl

class MainAdminSite(AdminSite):

    site_header = "FileShop Admin"
    site_title = "FileShop"
    index_title = "FileShop Admin"

    def has_permission(self, request):
        if not request.user.is_superuser:
            return False
        
        return True

admin_site = MainAdminSite(name="admin")


class OrderAdmin(ModelAdmin):

    list_display = ['uid', 'timestamp', 'product', 'crypto', 'address', 'is_payment_complete', 'usd_price', 'expected_value', 'status_of_transaction', 'txid', 'received_value']
    search_fields = ['address', 'txid', 'uid']
    list_filter = ['status_of_transaction', 'crypto']
    
    def has_change_permission(self, *args, **kwargs) -> bool:
        return False

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

class WithdrawlAdmin(ModelAdmin):

    list_display = ['uid', 'created_on', 'product', 'crypto', 'address', 'amount', 'status', 'txid', 'modified_on']
    search_fields = ['address', 'txid', 'uid']
    list_filter = ['status', 'crypto']
    readonly_fields = ['created_on', 'modified_on', 'crypto', 'address', 'amount', 'uid', 'product']

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False

admin_site.register(Order, OrderAdmin)
admin_site.register(Withdrawl, WithdrawlAdmin)
