from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import FilingList, Filing
from .tasks import process_filing_list


@receiver(post_save, sender=FilingList)
def process_filing_list_signal(sender, instance, created, **kwargs):
    pass
    # if not created:
    #     # https://stackoverflow.com/questions/45276828/handle-post-save-signal-in-celery
    #     transaction.on_commit(
    #         lambda: process_filing_list.apply_async(args=(instance.pk,))
    #     )


@receiver(post_delete, sender=FilingList)
def filing_list_file_delete(sender, instance, **kwargs):
    instance.datafile.delete(False)


@receiver(post_delete, sender=Filing)
def filing_file_dlete(sender, instance, **kwargs):
    instance.datafile.delete(False)
