const BASE = "http://localhost:8000"
const API_BASE = `${BASE}/api`

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
    download_url: `${BASE}/order/:order_uid/download`
}

export default apiendpoints