import json

from django.db.models import Prefetch
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache

from .forms import ProductForm
from .models import File, Order, Product
from .utils import email_helper, zipFiles

# Create your views here.


# =========================================================== Seller View ===================================================


class ProductCreateView(generic.View):
    form_class = ProductForm
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        """Depreciated, in favor of REST Endpoint"""
        product_form = self.form_class(request.POST or None)
        if product_form.is_valid():
            product = product_form.save()
            for _file in request.FILES.getlist("files"):
                file_obj = File.objects.create(
                    product=product, file_data=_file.file.read(), file_name=_file.name
                )
                request.session["product_id"] = product.pk
            return redirect(reverse("core:product_seller_email_updates"))
        else:
            return render(
                request, self.template_name, context={"errors": product_form.errors}
            )

    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


class ProductEmailUpdatesView(generic.TemplateView):

    template_name = "sell-email.html"

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
            status_of_transaction=Order.StatusChoices.CONFIMED
        )
        return context


# ===================================================== BUYER VIEW ============================================


class ProductPublicView(generic.TemplateView):

    template_name = "buyerLanding.html"

class IntializeOrder(generic.TemplateView):

    template_name = "buyerPay.html"

class OrderConfirmCallbackView(generic.View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        status_of_transaction = data.get("status", None)
        order_id = data.get("order_id", None)
        if status_of_transaction is None or order_id is None:
            return HttpResponse("Invalid data", status=400)

        order = get_object_or_404(Order, pk=int(order_id))

        if status_of_transaction >= order.status_of_transaction:
            order.status_of_transaction = max(
                order.status_of_transaction, status_of_transaction
            )
            order.save()
            return redirect(
                reverse(
                    "core:order_info_buyer", kwargs={"order_id": order.order_id}
                )
            )

        return HttpResponse("Order status isn't changed")

class OrderStatusView(generic.View):
    order_status_view = {
        0: "confirmation.html",
        1: "confirmation.html",
        2: "payStatus.html",
    }

    def get_order(self, **kwargs):
        order = get_object_or_404(Order, uid=self.kwargs.get("order_uid"))
        return order

    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        order = self.get_order(**kwargs)
        try:
            request.session["order"][
                "status_of_transaction"
            ] = order.status_of_transaction
            request.session.modified = True
        except KeyError:
            request.session["order"] = {
                "status_of_transaction": order.status_of_transaction
            }

        context = {
            "order": order,
            "download_uri": request.build_absolute_uri(
                reverse(
                    "core:order_info_buyer", kwargs={"order_id": order.order_id}
                )
            ),
        }

        return render(
            request,
            self.order_status_view[order.status_of_transaction],
            context=context,
        )


class DownloadFiles(generic.View):
    def get_order(self, **kwargs):
        orders = Order.objects.filter(order_id=kwargs["order_id"])
        if not orders.exists():
            raise Http404("Order with given order id does not exist")

        order = (
            orders.select_related("product")
            .prefetch_related(
                Prefetch(
                    "product__files",
                    queryset=File.objects.filter(
                        product__orders__order_id=kwargs["order_id"]
                    ),
                    to_attr="files_list",
                )
            )
            .first()
        )
        return order

    def get(self, request, *args, **kwargs):

        order = self.get_order(**kwargs)

        try:
            status_of_transaction = request.session["order"]["status_of_transaction"]
            if status_of_transaction == 2:
                files = order.product.files_list
                zipped_file = zipFiles(files)
                response = HttpResponse(
                    zipped_file, content_type="application/octet-stream"
                )
                response[
                    "Content-Disposition"
                ] = f"attachment; filename={order.product.product_name}.zip"
                return response
            else:
                return HttpResponse("Order is being processed")
        except KeyError:
            return HttpResponse("Session may have expired try refreshing", status=400)
        except Exception as e:
            repr(e)
            return HttpResponse(repr(e), status=400)


class UpdateOrderStatusCallback(generic.View):
    email_template = "emails/payment.html"
    email_subject = "emails/product_page.txt"
    extra_email_context = {}

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, address=request.GET["addr"])
        order.status_of_transaction = max(
            order.status_of_transaction, int(request.GET["status"])
        )
        order.txid = request.GET["txid"]
        if int(request.GET["status"]) == 2:
            order.received_value = float(request.GET["value"]) / 1e8
            self.extra_email_context["track_uri"] = self.request.build_absolute_uri(
                reverse(
                    "core:product_info_seller", kwargs={"token": order.product.token}
                )
            )
            email_helper(
                request,
                order.product.email,
                self.email_subject,
                self.email_template,
                html_email_template_name=self.email_template,
                extra_email_context=self.extra_email_context,
            )
        order.save()
        return HttpResponse(200)
