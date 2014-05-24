from post_office import mail
from post_office.management.commands import send_queued_mail
from celery.task import task

@task
def send_emails(num_processes=1):
    """
    check the mail queue and send the outgoing mail.
    this simply wraps the management command that comes with django-post-office
    """
    cmd = send_queued_mail.Command()
    cmd.execute(processes=num_processes)
