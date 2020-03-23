from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail

# Create your views here.


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        realtor_email = request.POST['realtor_email']
        user_id = request.POST['user_id']

        contact = Contact(listing_id=listing_id, listing=listing, name=name, email=email, phone=phone,
                          message=message, user_id=user_id)
        # check if the user user has made an inquiry or not
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing=listing, user_id=user_id)
            if has_contacted:
                messages.error(
                    request, 'You have already submitted an inquiry for this listing')
                return redirect('/listings/'+listing_id)

        contact.save()
        # send email
        send_mail(
            'Property listing Inquiry',
            'They has been an inquiry for' + listing +
            '. sign into the admin panel for more info.',
            'accesssquaretester2@gmail.com',
            [realtor_email, 'amodubashir17@gmail.com'],
            fail_silently=False
        )
        messages.success(
            request, 'Your request has been submitted a realtor will get back to you soon')

    return redirect('/listings/'+listing_id)
