from django.core import mail
from django_ilmoitin.models import NotificationTemplate
from parler.utils.context import switch_language


def assert_permission_denied(response):
    assert (
        response["errors"][0]["message"]
        == "You do not have permission to perform this action"
    )


def assert_mails_match_snapshot(snapshot):
    snapshot.assert_match(
        [f"{m.from_email}|{m.to}|{m.subject}|{m.body}" for m in mail.outbox]
    )


def create_notification_template_in_language(
    notification_type, language, **translations
):
    try:
        template = NotificationTemplate.objects.get(type=notification_type)
    except NotificationTemplate.DoesNotExist:
        template = NotificationTemplate(type=notification_type)
    with switch_language(template, language):
        for field, value in translations.items():
            setattr(template, field, value)
            template.save()

    return template
