import zipfile
import io
import os
from django.core.mail import EmailMultiAlternatives
from django.db.models.query import QuerySet
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from .blockonomics_utils import create_order, exchanged_rate, exchanged_rate_to_usd
from .models import Order
from datetime import datetime, timedelta


def zipFiles(files: QuerySet):
    outfile = io.BytesIO()
    with zipfile.ZipFile(outfile, "w") as zf:
        for f in files.iterator():
            with open(f.file_name, "wb") as file:
                file.write(f.file_data)
                file.close()
            zf.write(f.file_name)
            os.remove(f.file_name)
    return outfile.getvalue()


def send_mail(
    subject_template_name,
    email_template_name,
    context,
    from_email,
    to_email,
    html_email_template_name=None,
):

    subject = loader.render_to_string(subject_template_name, context)
    subject = "".join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")

    email_message.send()


def email_helper(
    request,
    email,
    subject_template_name,
    email_template_name,
    html_email_template_name=None,
    extra_email_context=None,
):
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain
    context = {
        "email": email,
        "domain": domain,
        "site_name": site_name,
        "protocol": "https" if request.is_secure() else "http",
        **(extra_email_context or {}),
    }

    send_mail(
        subject_template_name,
        email_template_name,
        context,
        settings.EMAIL_HOST_USER,
        email,
        html_email_template_name=html_email_template_name,
    )


def check_session_validity(request, product):
    last_order = request.session.get("last_order", None)
    if (
        last_order is None
        or datetime.now() - datetime.fromtimestamp(last_order) > timedelta(minutes=10)
        or request.session["order"]["product"] != product.pk
    ):
        raise ValueError("Invalid session value refreshing the sesion")


def create_order_helper(request, product, crypto, usd_price) -> Order:
    address, expected_value = create_order(product, crypto)
    usd_price = exchanged_rate_to_usd(expected_value, crypto, "USD")
    order = Order.objects.create(
        address=address, expected_value=expected_value, crypto=crypto, product=product, usd_price=usd_price
    )
    request.session["last_order"] = datetime.now().timestamp()
    return order
