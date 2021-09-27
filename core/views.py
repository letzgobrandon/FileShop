from django.http.response import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, reverse
from django.views import generic

from .models import Order, Product
from .utils import zipFiles

# Create your views here.


# =========================================================== Seller View ===================================================

class ProductSellerView(generic.DetailView):
    template_name = "pymnt-dash.html"
    model = Product

    def get_object(self, **kwargs):
        products = Product.objects.filter(token=self.kwargs.get("token"))
        if not products.exists():
            raise Http404("Product with given token does not exist")

        product = products.prefetch_related("orders").first()
        return product

    def get_context_data(self, **kwargs):
        context = super(ProductSellerView, self).get_context_data(**kwargs)
        context["btc_balance"] = context["object"].btc_balance
        # context["bch_balance"]=context["object"].bch_balance
        context["public_uri"] = self.request.build_absolute_uri(
            reverse("core:product_info_buyer", kwargs={"uid": context["object"].uid})
        )
        context["orders"] = context["object"].orders.filter(
            status_of_transaction=Order.StatusChoices.CONFIRMED
        )
        return context


# ===================================================== BUYER VIEW ============================================
class DownloadFiles(generic.View):

    def get_order(self, **kwargs):
        return get_object_or_404(Order, uid=kwargs['order_uid'])

    def get(self, request, *args, **kwargs):

        order = self.get_order(**kwargs)

        if order.status_of_transaction > order.StatusChoices.NOT_STARTED and order.is_payment_complete:
            files = order.product.product_files
            zipped_file = zipFiles(files)
            response = HttpResponse(
                zipped_file, content_type="application/octet-stream"
            )
            response[
                "Content-Disposition"
            ] = f"attachment; filename={order.product.product_name or 'Unnamed'}.zip"
            return response
        else:
            return HttpResponseForbidden("Error: Order is still being processed")
