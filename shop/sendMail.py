import os
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from smtplib import SMTPException
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa


def sendConfirmedMail(email, title, bookingid, tickets=[], api_type=None, extra=None):
    FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
    subject = "Booking Confirmed"
    if api_type.upper() == "V":
        message = f"Your Cuore Tours {title} Booking has been confirmed,  Your order id is {bookingid}, Here are the tickets tickets:\n"
        for ticket in tickets:
            message += f"- {ticket}\n"

    if api_type.upper() == "G":
        message = f"Your Cuore Tours {title} Booking has been confirmed,  Your order id is {bookingid} and type {api_type}, Collect your ticket from ticket counter"
    elif api_type.upper() == "B":
        message = f"Your Cuore Tours {title} Booking has been confirmed, {tickets}"
    else:
        message = f"Your Cuore Tours {title} Booking has been confirmed,  Your order id is {bookingid},  Here are the tickets {tickets}"
    try:
        res = send_mail(subject, message, FROM_EMAIL, [email])
    except:
        pass


def sendPaymentMail(email, title, reservation_id, amount):
    FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
    subject = "Cuore Tours Payment Successful"
    message = f"Your Cuore Tours {title} booking Payment {amount} has been paid, Your order id is {reservation_id}."
    try:
        send_mail(subject, message, FROM_EMAIL, [email])
    except:
        pass


def save_pdf(params):
    template = get_template("pdf.html")
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    return response


def sendVoucherMail(booking):
    try:
        FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
        subject = "Cuore Tours Booking Confirmed"
        message = f"Your Cuore Tours {booking.product_title} Booking has been confirmed,  Your order id is {booking.booking_id}"
        recipient_email = [booking.user.email]

        owner_info = {}

        context = {
            "booking": booking,
            "owner_info": owner_info,
            "participants": booking.participants.all(),
            "BASE_URL": f"{settings.SITE_URL}",
        }
        pdf_content = save_pdf(context)
        email = EmailMultiAlternatives(subject, message, FROM_EMAIL, recipient_email)
        email.attach("voucher.pdf", pdf_content.getvalue(), "application/pdf")
        res = email.send()
    except SMTPException as e:
        print(f"An error occurred while sending the email: {e}")
