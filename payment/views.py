from django.shortcuts import render, redirect
from payment.models import ShippingAddress, Order, OrderItem
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product, Profile
import datetime


def orders(request, pk):
    """
    View to display and update the status of a specific order.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        if request.POST:
            status = request.POST['shipping_status']
            if status == "true":
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order.update(shipped=False)
            messages.success(request, 'Your order has been successfully updated.')
            return redirect('home')
        return render(request, 'payment/orders.html', {'order': order, 'items': items})


def shipped_dash(request, pk=None):
    """
    View to display and update the shipped orders dashboard.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            now = datetime.datetime.now()
            order.update(shipped=False)
            messages.success(request, 'Your order has been successfully updated.')
            return redirect('home')

        if pk and request.method == 'POST':
            status = request.POST['shipping_status']
            order = Order.objects.get(id=pk)
            if status == 'true':
                order.shipped = True
            else:
                order.shipped = False
            order.save()
            messages.success(request, 'Your shipped order has been updated')
            return redirect('orders', pk=pk)

        return render(request, 'payment/shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, 'Access denied')
        return redirect('home')


def not_shipped_dash(request):
    """
    View to display and update the not shipped orders dashboard.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
            messages.success(request, 'Your order has been successfully updated.')
            return redirect('home')
        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, 'Access denied')
        return redirect('home')


def process_order(request):
    """
    Process the order by saving order and order items to the database.
    """
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = (
            f"{my_shipping['shipping_address1']}\n"
            f"{my_shipping['shipping_address2']}\n"
            f"{my_shipping['shipping_city']}\n"
            f"{my_shipping['shipping_state']}\n"
            f"{my_shipping['shipping_zipcode']}\n"
            f"{my_shipping['shipping_country']}"
        )
        amount_paid = totals

        if request.user.is_authenticated:
            user = request.user
            created_order = Order(
                user=user, full_name=full_name, email=email,
                shipping_address=shipping_address, amount_paid=amount_paid
            )
            created_order.save()
            order_id = created_order.pk

            for product in cart_products:
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price
                for key, value in quantities.items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id, product_id=product_id,
                            user=user, price=price, quantity=value
                        )
                        create_order_item.save()

            # Clear session cart data
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session['session_key']

            currernt_user = Profile.objects.filter(user__id=request.user.id)
            currernt_user.update(old_cart="")

            messages.success(request, 'Order placed')
            return redirect('home')
        else:
            created_order = Order(
                full_name=full_name, email=email,
                shipping_address=shipping_address, amount_paid=amount_paid
            )
            created_order.save()

            order_id = created_order.pk
            for product in cart_products:
                product_id = product.id
                price = product.sale_price if product.is_sale else product.price
                for key, value in quantities.items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id, product_id=product_id,
                            price=price, quantity=value
                        )
                        create_order_item.save()

            # Clear session cart data
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session['session_key']

            messages.success(request, 'Order placed')
            return redirect('home')

    else:
        messages.success(request, 'Access denied')
        return redirect('home')


def billing_info(request):
    """
    Collect billing information and display the billing form.
    """
    if request.method == 'POST':
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        billing_form = PaymentForm()
        return render(request, 'payment/billing_info.html', {
            'cart_products': cart_products,
            'quantities': quantities,
            'totals': totals,
            'shipping_info': request.POST,
            'billing_form': billing_form
        })
    else:
        messages.success(request, 'Access denied')
        return redirect('home')


def checkout(request):
    """
    Handle the checkout process, including displaying and saving shipping information.
    """
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        try:
            shipping_user = ShippingAddress.objects.get(user=request.user)
            if request.method == 'POST':
                shipping_form = ShippingForm(request.POST, instance=shipping_user)
                if shipping_form.is_valid():
                    shipping_form.save()
                    return redirect('billing_info')
            else:
                shipping_form = ShippingForm(instance=shipping_user)
        except ShippingAddress.DoesNotExist:
            if request.method == 'POST':
                shipping_form = ShippingForm(request.POST)
                if shipping_form.is_valid():
                    shipping_info = shipping_form.save(commit=False)
                    shipping_info.user = request.user
                    shipping_info.save()
                    return redirect('billing_info')
            else:
                shipping_form = ShippingForm()
    else:
        shipping_form = ShippingForm(request.POST or None)

    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
        'shipping_form': shipping_form,
    }

    return render(request, 'payment/checkout.html', context)


def payment_success(request):
    """
    Display the payment success page.
    """
    return render(request, 'payment/payment_success.html')
