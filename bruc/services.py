import io
import logging
import smtplib
import socket
from email.mime.image import MIMEImage
from email.utils import make_msgid

import segno

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from .models import Mailer

logger = logging.getLogger(__name__)

GUEST_TICKET_SUBJECT = "[#BRUCIFER26] Potvrda za kupljenu kartu"
QR_CID = 'ticket-qr@brucifer'

DIACRITICS = {'č': 'c', 'š': 's', 'ž': 'z', 'đ': 'd', 'ć': 'c'}


def derive_fer_email(name, surname, jmbag):
    """Port of ui/src/utils/ferEmail.js — keep the two in sync."""
    name = (name or '').strip()
    surname = (surname or '').strip()
    jmbag = (jmbag or '').strip()
    if not name or not surname or not jmbag:
        return None

    digits = jmbag[4:9] if jmbag.startswith('003') else jmbag[:9]
    initials = ''.join(DIACRITICS.get(c, c) for c in (name[0].lower(), surname[0].lower()))
    return f"{initials}{digits}@fer.hr"


MAIL_TEMPORARY_ERROR = 'Brevo privremeno odbija slanje, pokušaj ponovno'
MAIL_REJECTED_ERROR = 'Brevo odbio poruku'


def classify_mail_error(exc):
    """Short Croatian reason shown to the seller; the full exception goes to the log."""
    if isinstance(exc, smtplib.SMTPRecipientsRefused):
        codes = [code for code, _ in exc.recipients.values()]
        if codes and all(400 <= code < 500 for code in codes):
            return MAIL_TEMPORARY_ERROR
        return 'adresa odbijena'
    if isinstance(exc, smtplib.SMTPAuthenticationError):
        return 'greška u autentikaciji mail servera'
    if isinstance(exc, (socket.timeout, ConnectionError, smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError)):
        return 'mail server nedostupan'
    # Rejections at MAIL FROM / DATA: rate limits (4xx), suspended account or content filter (5xx)
    if isinstance(exc, smtplib.SMTPResponseException):
        if 400 <= exc.smtp_code < 500:
            return MAIL_TEMPORARY_ERROR
        if 500 <= exc.smtp_code < 600:
            return MAIL_REJECTED_ERROR
    return 'nepoznata greška'


def build_ticket_qr_png(conf_code):
    buf = io.BytesIO()
    segno.make_qr(conf_code, error='m').save(buf, kind='png', scale=8, border=4)
    return buf.getvalue()


def send_guest_ticket_email(guest):
    """Send the ticket mail and record the outcome on the guest. Returns (ok, reason)."""
    to = derive_fer_email(guest.name, guest.surname, guest.jmbag)
    if not to:
        reason = 'nedostaje ime, prezime ili JMBAG'
        guest.mailStatus, guest.mailError = 'failed', reason
        guest.save(update_fields=['mailStatus', 'mailError'])
        return False, reason

    html_message = render_to_string('emails/guest_email.html', {
        'name': guest.name, 'confCode': guest.confCode, 'qrCid': QR_CID})
    message_id = make_msgid(domain='kset.org')
    msg = EmailMultiAlternatives(
        GUEST_TICKET_SUBJECT, strip_tags(html_message),
        f"43. Brucifer <{settings.DEFAULT_FROM_EMAIL}>", [to],
        headers={'Message-ID': message_id})
    msg.attach_alternative(html_message, "text/html")
    msg.mixed_subtype = 'related'
    qr = MIMEImage(build_ticket_qr_png(guest.confCode), 'png')
    qr.add_header('Content-ID', f'<{QR_CID}>')
    qr.add_header('Content-Disposition', 'inline', filename='karta.png')
    msg.attach(qr)

    try:
        msg.send()
    except Exception as exc:
        logger.exception("Ticket mail to guest %s failed", guest.pk)
        reason = classify_mail_error(exc)
        guest.email, guest.mailStatus, guest.mailError = to, 'failed', reason
        guest.save(update_fields=['email', 'mailStatus', 'mailError'])
        return False, reason

    guest.email = to
    guest.mailStatus, guest.mailError = 'sent', ''
    guest.mailSentAt = timezone.now()
    guest.mailMessageId = message_id
    guest.save(update_fields=['email', 'mailStatus', 'mailError', 'mailSentAt', 'mailMessageId'])
    Mailer.objects.create(
        subject=GUEST_TICKET_SUBJECT,
        message=f"{guest.name} {guest.surname} {guest.confCode}",
        to_mail=to)
    return True, None
