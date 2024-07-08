from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    """
    Render the cart summary page.
    """
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals
    })


def cart_add(request):
    """
    Add a product to the cart and return the updated cart quantity as JSON.
    """
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()

        # Return the updated cart quantity as JSON response
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, "Product added to cart")
        return response


def cart_delete(request):
    """
    Delete a product from the cart and return the product ID as JSON.
    """
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)

        # Return the product ID that was deleted as JSON response
        response = JsonResponse({'product': product_id})
        messages.success(request, "Product deleted from cart")
        return response


def cart_update(request):
    """
    Update the quantity of a product in the cart and return the updated quantity as JSON.
    """
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity=product_qty)

        # Return the updated quantity as JSON response
        response = JsonResponse({'qty': product_qty})
        messages.success(request, "Product updated")
        return response
