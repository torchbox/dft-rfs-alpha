from datetime import datetime
from dateutil.relativedelta import relativedelta

from notifications_python_client.notifications import NotificationsAPIClient

from django import forms
from django.conf import settings
from django.template.response import TemplateResponse
from django.views import defaults


def page_not_found(request, exception, template_name="patterns/pages/errors/404.html"):
    return defaults.page_not_found(request, exception, template_name)


def server_error(request, template_name="patterns/pages/errors/500.html"):
    return defaults.server_error(request, template_name)


class NotifyTestForm(forms.Form):
    name = forms.CharField(
            label="First name",
            required=True,
            max_length=255
        )
    reg = forms.CharField(
            label="Registration mark",
            required=True,
            max_length=255
        )
    pin = forms.CharField(
            label="PIN",
            required=True,
            max_length=255
        )


def notify_test(request, template_name="notify_test.html"):

    msg = None
    api_key = getattr(settings, "NOTIFY_API_TEST_KEY_SEND", None)
    email_template_id = getattr(settings, "NOTIFY_EMAIL_TEMPLATE_ID", None)
    email_address = getattr(settings, "NOTIFY_EMAIL_ADDRESS", None)
    expected_pin = getattr(settings, "NOTIFY_DEMO_PIN", None)

    def _send():
        notifications_client = NotificationsAPIClient(api_key)
        submission_date = datetime.now()
        read_close_date = submission_date + relativedelta(months=6)
        response = notifications_client.send_email_notification(
            email_address=email_address,
            template_id=email_template_id,
            personalisation={
                "first_name": form.cleaned_data["name"],
                "registration_mark": form.cleaned_data["reg"],
                "submission_date": submission_date.strftime("%d %B %Y"),
                "read_close_date": read_close_date.strftime("%d %B %Y"),
                "survey_url": "https://example.com/xyz"
            }
        )
        return response["id"]

    if request.method == "POST":
        form = NotifyTestForm(request.POST)
        msg = "Invalid details"
        if form.is_valid() and form.cleaned_data["pin"] == expected_pin:
            send_id = _send()
            msg = f"Sent ({send_id})"
    else:
        if api_key and email_template_id:
            form = NotifyTestForm()
        else:
            form = None
            msg = "Notify API not configured"
    return TemplateResponse(request, template_name, {
        "form": form,
        "msg": msg
    })
