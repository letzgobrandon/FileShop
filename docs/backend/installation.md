# Backend - Installation

Follow the instructions below to setup your API Server.

## Requirements
Make sure you have [Python](https://www.python.org/downloads/) and [Pip](https://pip.pypa.io/en/latest/installing/#installing-with-get-pip-py) installed. Python version >= 3.6 is required.

You also need Django, and other dependencies. These can be installed by running:

```
pip install -r requirements.txt 
```

### Variables and Tokens

All tokens and customisable/overriden Django Settings are read from `satoshi_box/local_settings.py`. This file is not tracked by GIT and hence a `sample_local_settings.py` file is provided in the same directory for easy configuration.

You can override any django setting using the file. The following variables are however required.

#### SECRET KEY

Add/Update the `SECRET_KEY` variable. The [Secret Key](https://docs.djangoproject.com/en/dev/ref/settings/#secret-key) is required to sign the app, Django will refuse to start if `SECRET_KEY` is not set. This [website](https://miniwebtool.com/django-secret-key-generator/) can be used to generate a unique `SECRET_KEY`. 

#### Blockonomics API Key and Callback Secret

Add/Update the `BLOCKONOMICS_API_KEY` variable. The API Key can be received from your [Merchant Store Dashboard](https://www.blockonomics.co/merchants#/stores)

Add/Update the `CALLBACK_SECRET` variable. This secret is used to validate the callbacks from Blockonmomics Server.

Blockonomics Callback URL will be `<protocol>//<your_domain>/api/order/callback/?secret=<your_CALLBACK_SECRET>` e.g. `https://api.example.com/api/order/callback/?secret=1234567899`

#### CORS/CSRF Settings

Add/Update CORS/CSRF Settings using the following variables:

```python
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https?:\/\/fileshop.online$"
]

CORS_ALLOWED_ORIGINS = [
    "http://fileshop.online",
    "https://fileshop.online",
]
```

You can replace filsehop.online with you own domain. For localhost use the following:

```python
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https?:\/\/localhost(:[0-9]{1,4})?$"
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost",
]
```

#### Email Settings

Add/Update the following Settings as per your Mail Server Configuration:

```python
EMAIL_USE_TLS = True
EMAIL_HOST = 'YOUR_HOST_NAME'
EMAIL_HOST_USER = 'YOUR_USER_NAME'
EMAIL_HOST_PASSWORD = 'YOUR_PASS'
EMAIL_PORT = 587
```

If you want to use GMail for Sending Mails, use the following configuration (Ref: https://support.google.com/mail/answer/7126229?hl=en)

```python
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'your_password'
EMAIL_PORT = 587
```

#### Deployment URL

Add/Update the `DEPLOYMENT_URL` variable to point your Frontend Application URL without trailing slash.

e.g.

```python
# For api.fileshop.online, we've our frontend at https://filsehop.online

DEPLOYMENT_URL = "https://fileshop.online"
```

### Setting up Database

After you have defined the variables mentioned above, nativate to your FileShop folder with your terminal and run:

```
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

If you want to use MySQL Database, use the following configuration in `local_settings.py` before running the commands above:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DATABASE_NAME',
        'USER': 'DATABASE_USER',
        'PASSWORD': 'DATABASE_PASSWORD',
        'HOST': 'DATABASE_HOST',
        'PORT': '3306'
    }
}
```
Update the DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABABE_HOST above with your configuration.

### Running server

Lastly, you can start the server by running:
```
python manage.py runserver 8000
```
