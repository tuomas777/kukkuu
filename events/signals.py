from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from events.models import Enrolment
from events.notifications import NotificationType
from events.utils import send_event_notifications_to_guardians


@receiver(post_save, sender=Enrolment)
def send_enrolment_email(instance, created, **kwargs):
    if created:
        guardians = instance.child.guardians.all()
        send_event_notifications_to_guardians(
            instance.occurrence.event,
            NotificationType.OCCURRENCE_ENROLMENT,
            guardians,
            child=instance.child,
            occurrence=instance.occurrence,
        )


@receiver(post_delete, sender=Enrolment)
def send_unenrolment_email(instance, **kwargs):
    guardians = instance.child.guardians.all()
    send_event_notifications_to_guardians(
        instance.occurrence.event,
        NotificationType.OCCURRENCE_UNENROLMENT,
        guardians,
        child=instance.child,
        occurrence=instance.occurrence,
    )
