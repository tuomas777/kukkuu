import pytest
from messaging.factories import MessageFactory
from messaging.models import Message
from parler.utils.context import switch_language

from common.tests.conftest import *  # noqa


@pytest.fixture
def message():
    message = MessageFactory(
        subject="Otsikko", body_text="Ruumisteksti.", recipient_selection=Message.ALL
    )
    with switch_language(message, "en"):
        message.subject = "Subject"
        message.body_text = "Body text."
        message.save()
    return message
