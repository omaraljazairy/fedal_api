from django.core.mail import EmailMultiAlternatives
import logging

logger = logging.getLogger('mail')

def send(sender=str, to=list, cc=list, bcc=list, subject=str, body=str, content_type='text', connection=None, headers=dict,
         reply_to=list, attachments=list):
    """
    a service to send emails as text or html format. Te content-type determines the body type of the email.
    :param sender: the sender email from who the email is sent.
    :param to: a list of emails to whome the email should be sent.
    :param cc: (optional) a list of emails to whome the email should be sent.
    :param bcc: (optional) a list of emails to whome the email should be sent.
    :param body: a string that is the body of the email.
    :param content_type: default type is text, but can also be html to send an html email.
    :param connection: An email backend instance. Use this parameter if you want to use the same connection for
                       multiple messages. If omitted, a new connection is created when send() is called.
    :param headers: (optional) headers if needed with the email.
    :param reply_to: (optional) list of emails to reply to.
    :return: a dict with status and msg keys.
    """

    try:
        msg = EmailMultiAlternatives(subject=subject, body=body, from_email=sender, to=to, bcc=bcc,
                                     connection=connection, attachments=attachments, content_type=content_type,
                                     cc=cc, headers=headers, reply_to=reply_to)
        msg.send(fail_silently=False)
        logger.debug("email sent")
        return {'status': 'OK', 'message': "email sent"}
    except Exception as e:
        logger.error("error sending email: %s" % e)
        return {'status': 'ERROR', 'message': str(e)}
