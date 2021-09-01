const API_BASE = "http://localhost:8000/api"

export const apiendpoints = {
    product_create: `${API_BASE}/product`,
    product_get: `${API_BASE}/product`,
    product_seller_email_update: `${API_BASE}/email_updates`,
    // currency_converter: `${API_BASE}/currency-converter`,
    order_create: `${API_BASE}/order`,
    order_get: `${API_BASE}/order/:order_uid`,
    order_callback: `${API_BASE}/order/:order_uid/callback`,
}

export const static_urls = {
    email_update: 'dashboard/email_updates',
    product_public_url: 'product/:uid',
    seller_dashboard: 'dashboard/:token',
    checkout: 'checkout/:order_uuid',
    order_confirm_callback: 'order_processed',
}

export default apiendpoints