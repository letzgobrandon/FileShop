# API Specs

This document contains all the API Endpoints (made till date and the respective models they use)

This Document is divided into two Segments:
- API LIST: Contains list of All API Endpoints till date
- Objects: Contains list of All Response Objects frequently returned.


API List
===
All APIs are listed below

# /api/product

This API is used to Create a Product Object

**Reversable Name:** `core:api_product_create`

**Depended Models:** `core.models.Product`, `core.models.File`

**Supported Methods:** POST

## POST

**Request Body**

| Param               | Type             | Required | Description                                         | Example                        |
|---------------------|------------------|----------|-----------------------------------------------------|--------------------------------|
| product_name        | String           | No       | Name of the Product                                 | MS Office 365 Single User      |
| product_description | String           | No       | Description of the Product                          | Unlocked Lifetime Free Edition |
| price               | Float            | Yes      | Price of the Product in selected currency           | 20                             |
| currency            | String [Choices] | Yes      | A valid supported currency. Currently Supports: USD | USD                            |
| files               | File [Array]     | Yes      | An Array of Files. Atleast 1 File is required.      | <File>                         |

**Response**

Status Code: 201

| Param               | Type             | Description                                         | Example                        |
|---------------------|------------------|-----------------------------------------------------|--------------------------------|
| uuid        | String (UUID)           | UUID of the Product | 123e4567-e89b-12d3-a456-426614174000 |
| token | String (UUID) | Secret Token of the Product to perform updates on the product | 123e4567-e89b-12d3-a456-426614174000 |

# /api/product/:uid

**Reversable Name:** `core:api_product`

**Depended Models:** `core.models.Product`

**Supported Methods:** GET, PATCH

## GET

This API is used to get the details of about a product using UID of the Product.

**Request Params**

| Param               | Type             | Required | Description                                         | Example                        |
|---------------------|------------------|----------|-----------------------------------------------------|--------------------------------|
| token        | String (UUID)          | No       | Token of the Product | 123e4567-e89b-12d3-a456-426614174000 |

**Response**

Status Code: 200

Returns a `ProductSensitive` Object if `token` is present in Request otherwise returns `Product` object.

Status Code: 404

Returns when the Product is not Found

## PATCH

This API is used to Update Information of the Product. Token of the product is required to process the update.


**Request Body**

| Param               | Type             | Required | Description                                         | Example                        |
|---------------------|------------------|----------|-----------------------------------------------------|--------------------------------|
| token        | String (UUID)          | Yes       | Token of the Product | 123e4567-e89b-12d3-a456-426614174000 |
| email        | String (Email)          | No       | Email to Update | xyz@example.com      |
| product_name        | String           | No       | Name of the Product | MS Office    |
| product_description | String           | No       | Description of the Product | Description of the Product |
| price               | Float            | No      | Price of the Product in selected currency           | 20                             |
| currency            | String [Choices] | No      | A valid supported currency. Currently Supports: USD | USD                            |

**Response**

Status Code: 200

Returns Empty Response



# /api/order

**Reversable Name:** `core:api_order_create`

**Depended Models:** `core.models.Product`, `core.models.Order`

**Supported Methods:** POST

## POST

This API is used to start a new Order for buying the Product. It creates a Order Object and returns the Order UUID for order.

**Request Body**

| Param               | Type             | Required | Description                                         | Example                        |
|---------------------|------------------|----------|-----------------------------------------------------|--------------------------------|
| crypto        | String           | Yes       | Crypto to Buy Using, Currently Supported Values are: BTC | BTC |
| product_uid        | String (UUID)         | Yes       | UID of the product to create order for | 	123e4567-e89b-12d3-a456-426614174000  |

**Response**

Status Code: 200

| Param               | Type             | Description                                         | Example                        |
|---------------------|------------------|-----------------------------------------------------|--------------------------------|
| order_uuid | String (UUID)           | UUID of the Order Created | 123e4567-e89b-12d3-a456-426614174000 |

# /api/order/:uid

**Reversable Name:** `core:api_order`

**Depended Models:** `core.models.Product`, `core.models.Order`

**Supported Methods:** GET

## GET

This API is used to get the details of a order. 

Does not accept any parameters.

# /api/order/callback

This endpoint serves as a callback URL for Blockonomics Store to notify the status of transaction.

**Reversable Name:** `core:api_order_blockonomics_callback`

**Depended Models:** core.models.Order

**Supported Methods:** GET

## GET

**Request Body**

| Param               | Type             | Required | Description                                         | Example                        |
|---------------------|------------------|----------|-----------------------------------------------------|--------------------------------|
| secret        | String           | Yes       | Fraud Prevent Secret Token as defined in settings.CALLBACK_SECRET | sdsdett4534g34rtf4 |
| txid       | String           | Yes       | Transaction ID |  |
| value        | Float           | Yes       | Received Value of Crypto | 123 |
| status        | Integer           | Yes       | Status of Transaction, valid range: [0,2] | 2 |
| addr        | String           | Yes       | BTC address of the transaction | dwrr237y329yc923tr923 |

**Response**

Status Code: 200, 

Returns Empty Response on 200, or Error Message on 403

# /api/currency-converter 

**DEPRECIATED AND REMOVED** 

This API used to convert source currency (e.g. 20 USD) to Target Currency (e.g. BTC). It doesn't create any order or address.

**Reversable Name:** `core:api_currency_converter`

**Depended Models:** None

**Supported Methods:** POST

## POST

**Request Body**

| Param               | Type             | Required | Description                                         | Example                        |
|---------------------|------------------|----------|-----------------------------------------------------|--------------------------------|
| currency        | String           | Yes       | Source Currency to Convert From, Currently Supported Values are: USD | USD |
| price        | Float           | Yes       | Amount to to Convert | 20 |
| crypro        | String           | Yes       | Target Crypto to Convert the currency to. Current Supported values are: BTC | BTC |

**Response**

Status Code: 200

| Param               | Type             | Description                                         | Example                        |
|---------------------|------------------|-----------------------------------------------------|--------------------------------|
| bits | Float           | Converted Amount in Bits |  
| price | Float           | Converted Amount in Target Currency (bits/pow(10, 8)) | 0.0001344 |


# Objects

## Product

| Param               | Type             | Description                                         | Example                        |
|---------------------|------------------|-----------------------------------------------------|--------------------------------|
| product_name        | String           | Name of the Product                                 | MS Office 365 Single User      |
| product_description | String           | Description of the Product                          | Unlocked Lifetime Free Edition |
| price               | Float            | Price of the Product in selected currency           | 20                             |
| currency            | String [Choices] | A valid supported currency. Currently Supports: USD | USD                            |
| num_files           | Integer          | Number of files uploaded in the Product             | 2                              |

## ProductSensitive

| Param               | Type             | Description                                         | Example                        |
|---------------------|------------------|-----------------------------------------------------|--------------------------------|
| uid                 | String (UUID)      | UUID of the Product            |                         |
| token               | String (UUID)      | Token of the Product           |                         |
| email               | String (Email)     | Email registered with Product  |                         |
| product_name        | String             | Name of the Product            |MS Office 365 Single User|
| product_description | String             | Description of the Product     | Unlocked Lifetime Free  |
| price               | Float              | Price of the Product in selected currency | 20           |
| currency            | String [Choices]   | A valid supported currency. Currently Supports: USD | USD|
| num_files           | Integer            | Number of files uploaded in the Product             | 2 |
| files               | Array [File]       | An Array of `File` Object in Product                | [] |

## File

| Param               | Type             | Description                                         | Example                        |
|---------------------|------------------|-----------------------------------------------------|--------------------------------|
| uid                 | String (UUID)      | UUID of the File            |                         |
| file_name           | String             | Name of the File            |xyz.doc |


## Order

| Param               | Type             | Description                                         | Example                        |
|---------------------|------------------|-----------------------------------------------------|--------------------------------|
| uid        | String (UUID)        | UUID of the Order                              |      |
| status_of_transaction | Integer (Choices)           | Status of Order, Choices: NOT_STARTED (-1), UNCONFIRMED (0), PARTIAL_CONFIRMED (1), CONFIRMED (2)                          | -1 |
| expected_value               | Float            | Expected Price to recevie in selected crypto           | 0.0000012                             |
| usd_price            | Float | Price in USD for Order | 20                            |
| received_value           | Float            | Actual Received Price in selected crypto           | 0.0000012                             |
| address           | String            | Payment Address           | sd87g389rv723y9r362vt92357v                             |
| crypto           | String            | Crypto used to create the order           | BTC |
| timestamp | Datetime | Date Time when the Order was last modified (ISO8601 Format) | 2000-10-31T01:30:00.000-05:00 | 
| product_uid           | String            | Product UID of the Order           | sdsfd23vetb36nb5 |
| product           | Object -> Product            | Product Object or None (if status_of_transaction != 2) | sdsfd23vetb36nb5 |
