from django.urls import path, re_path
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
        r"^checkout/(?P<order_uid>[0-9a-f-]+)$",
        views.IntializeOrder.as_view(),
        name="product_pay_buyer",
    ),
    re_path(
        r"^order_processed/$",
        views.OrderConfirmCallbackView.as_view(),
        name="order_processed_buyer",
    ),
    re_path(
        r"^order/(?P<order_uid>[0-9a-f-]+)/$",
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

    re_path(
        r"^api/product$",
        api_views.ProductCreateAPIView.as_view(),
        name="api_product_create",
    ),
    re_path(
        r"^api/product/(?P<uid>[0-9a-f-]+)$",
        api_views.ProductAPIView.as_view(),
        name="api_product",
    ),
    re_path(
        r"^api/order$",
        api_views.InitiateProductBuyAPIView.as_view(),
        name="api_product_order",
    ),
    re_path(
        r"^api/order/(?P<uid>[0-9a-f-]+)$",
        api_views.OrderAPIView.as_view(),
        name="api_order",
    ),
    re_path(
        r"^api/order/(?P<uid>[0-9a-f-]+)/callback$",
        api_views.OrderConfirmCallbackAPIView.as_view(),
        name="api_order_callback",
    ),
    # re_path(
    #     r"^api/currency-converter$",
    #     api_views.CurrencyConverterAPIView.as_view(),
    #     name="api_currency_converter",
    # ),
]
