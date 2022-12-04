import stripe

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings

from .models import Product


def get_product_list(request):
    products = Product.objects.all()
    return render(request, "shop/product_list.html", context={
        "products": products
    })


@require_POST
def add_to_cart(request: HttpRequest) -> HttpResponse:
    product_id = request.POST["product_id"]
    cart = request.session.get("shopping_cart", {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session["shopping_cart"] = cart
    request.session.modified = True
    return redirect("product_list")


def get_cart_items(request):
    cart = request.session.get("shopping_cart", {})
    product_ids = [int(key) for key in cart.keys()]
    products = Product.objects.filter(pk__in=product_ids).all()
    items = []
    for product in products:
        quantity = int(cart.get(str(product.pk)))
        item = {
            "name": product.name,
            "quantity": quantity,
            "price": product.price,
            "total": product.price * quantity,
        }
        items.append(item)
    return render(request, "shop/cart.html", context={
        "items": items
    })


@require_GET
def get_stripe_config(request):
    config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
    return JsonResponse(config)


@require_GET
def create_checkout_session(request):
    domain_url = 'http://localhost:8000/'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - capture the payment later
        # [customer_email] - prefill the email input in the form
        # For full details see https://stripe.com/docs/api/checkout/sessions/create


        cart = request.session.get("shopping_cart", {})
        product_ids = [int(key) for key in cart.keys()]
        products = Product.objects.filter(pk__in=product_ids).all()
        items = []
        for product in products:
            quantity = int(cart.get(str(product.pk)))
            item = {
                "quantity": quantity,
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product.name,
                        "description": product.description,
                    },
                    "unit_amount": str(int(product.price * 100)),
                }
            }
            items.append(item)

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + 'shop/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + 'shop/cancel/',
            payment_method_types=['card'],
            mode='payment',
            line_items=items
        )
        return JsonResponse({'sessionId': checkout_session['id']})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def payment_success(request):
    request.session["shopping_cart"] = {}
    request.session.modified = True
    return render(request, "shop/success.html")


def payment_cancel(request):
    return render(request, "shop/cancel.html")