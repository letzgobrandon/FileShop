from django.urls import path, include, re_path
from . import views, api_views

app_name = "core"
urlpatterns = [
    path("", views.ProductCreateView.as_view(), name="product_create_view"),
    re_path(
        r"^dashboard/(?P<token>[0-9a-f-]+)$",
        views.ProductSellerView.as_view(),
        name="product_info_seller",
    ),
    re_path(
        r"^dashboard/email_updates$",
        views.ProductEmailUpdatesView.as_view(),
        name="product_seller_email_updates",
    ),
    re_path(
        r"^product/(?P<uid>[0-9a-f-]+)/$",
        views.ProductPublicView.as_view(),
        name="product_info_buyer",
    ),
    re_path(
        r"^checkout/(?P<order_id>\w+)$",
        views.IntializeOrder.as_view(),
        name="product_pay_buyer",
    ),
    re_path(
        r"^order_processed/$",
        views.OrderConfirmCallbackView.as_view(),
        name="order_processed_buyer",
    ),
    re_path(
        r"^order/(?P<order_id>\w+)/$",
        views.OrderStatusView.as_view(),
        name="order_info_buyer",
    ),
    re_path(
        r"^(?P<order_id>\w+)/download/$",
        views.DownloadFiles.as_view(),
        name="product_download_buyer",
    ),
    path(
        "update/orders",
        views.UpdateOrderStatusCallback.as_view(),
        name="order_status_update",
    ),

    ## API URLs Start ##

    path(
        "api/product",
        api_views.ProductCreateAPIView.as_view(),
        name="api_product_create_view",
    ),
    path(
        "api/email_updates",
        api_views.EmailUpdateAPIView.as_view(),
        name="api_product_seller_email_updates",
    ),
    re_path(
        r"^api/product/(?P<uid>[0-9a-f-]+)$",
        api_views.ProductPublicAPIView.as_view(),
        name="api_product_info_buyer",
    ),
    re_path(
        r"^api/product/(?P<uid>[0-9a-f-]+)/initiate-transaction$",
        api_views.InitiateProductBuyAPIView.as_view(),
        name="api_product_initiate_transaction",
    ),
    re_path(
        r"^api/currency-converter$",
        api_views.CurrencyConverterAPIView.as_view(),
        name="api_currency_converter",
    ),
]
