from django.core.mail import send_mail
from .models import Order, Customer
from dotch__in.celery import app
from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@app.task()
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """

    order = Order.objects.get(id=order_id)


    subject = 'Dotch.in- Order Number. {}'.format(order.id)

    name = order.customer.first_name
    oid = order_id
    code = order.customer.referral_code

    context = {'name':name, 'oid':oid, 'code':code}


    html_content = render_to_string('review_form.html', {'name':name, 'oid':oid, 'code':code})
    text_content = strip_tags(html_content)
    message = EmailMultiAlternatives(subject, text_content, 'rachelselv@gmail.com', [order.customer.email])
    message.attach_alternative(html_content, 'text/html')
    message.send()

    return message

@app.task()
def order_created_admin(order_id):
    """
    Task to send an e-mail notification to admin when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Good day!\n\nAn order has been placed.\
    The order id is {}.'.format(order.id)
    mail_sent = send_mail(subject,
                          message,
                          'rachelselv@gmail.com',
                          ['likhithkosini@dotch.in'])
    return mail_sent


@app.task()
def free_service(order_id, customer_id):
    """
    Task to send an e-mail notification when an 5 successful orders are done.
    """
    order = Order.objects.get(id=order_id)
    referrer = Customer.objects.get(id=customer_id)
    subject = 'Free service on order nr. {}'.format(order.id)
    message = 'Good day!\n\nA customer has been awarded free service.\
    The order id is {}. The customer is {} with ID {}'.format(order.id, referrer.referral_code,customer_id)
    mail_sent = send_mail(subject,
                          message,
                          'rachelselv@gmail.com',
                          ['likhithkosini@dotch.in'])
    return mail_sent


@app.task()
def free_service_11(order_id):
    """
    Task to send an e-mail notification when an 5 successful orders are done.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Free service for order nr. {}'.format(order.id)
    message = 'Good day!\n\nAn order has been awarded free service for first 11 orders.\
    The order id is {}.'.format(order.id)
    mail_sent = send_mail(subject,
                          message,
                          'rachelselv@gmail.com',
                          ['s_rachel53@hotmail.com'])
    return mail_sent

