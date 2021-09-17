from django.urls import path, re_path
from . import views, api_views

app_name = "core"
urlpatterns = [
    re_path(
        r"^dashboard/(?P<token>[0-9a-f-]+)$",
        views.ProductSellerView.as_view(),
        name="product_info_seller",
    ),
    re_path(
        r"^order/(?P<order_uid>[0-9a-f-]+)/download/$",
        views.DownloadFiles.as_view(),
        name="product_download_buyer",
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
        r"^api/product/(?P<token>[0-9a-f-]+)/orders$",
        api_views.ProductOrdersListAPIView.as_view(),
        name="api_product_orders",
    ),
    re_path(
        r"^api/product/(?P<token>[0-9a-f-]+)/balances$",
        api_views.ProductBalancesAPIView.as_view(),
        name="api_product_balances",
    ),
    re_path(
        r"^api/product/(?P<token>[0-9a-f-]+)/withdrawls$",
        api_views.ProductWithdrawlsListAPIView.as_view(),
        name="api_product_withdrawls",
    ),
    re_path(
        r"^api/product/(?P<token>[0-9a-f-]+)/withdrawl$",
        api_views.ProductWithdrawAPIView.as_view(),
        name="api_product_withdrawl",
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
        r"^api/order/callback/$",
        api_views.OrderCallbackView.as_view(),
        name="api_order_blockonomics_callback",
    ),
    # re_path(
    #     r"^api/currency-converter$",
    #     api_views.CurrencyConverterAPIView.as_view(),
    #     name="api_currency_converter",
    # ),
]
