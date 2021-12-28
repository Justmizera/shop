import stripe

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from .cart import Cart
from .forms import CheckoutForm

from apps.order.utilities import checkout

def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            place = form.cleaned_data['place']

            order = checkout(request, first_name, last_name, email, address, zipcode, place, phone, cart.get_total_cost())

            send_mail(
            'Potwierdzenie złożenia zamówienia',
            'Potwierdzam to, że zamówienie zostało złożone',
            'tt670165@gmail.com',
            [email],
            fail_silently= False
            )

            cart.clear()


            return redirect('success')
    
    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')

    return render(request, 'cart/cart.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})


def success(request):
    return render(request, 'cart/success.html')

def orderForm(request):
    return render(request, 'cart/orderForm.html')
