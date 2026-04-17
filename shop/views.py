from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import json
from collections import defaultdict

from .models import Product, Contact, Orders, OrderUpdate


@login_required
def index(request):
    products = Product.objects.all()

    # group by category
    catprods = defaultdict(list)

    for product in products:
        catprods[product.category_name].append(product)

    allprods = []

    for cat, prods in catprods.items():
        n = len(prods)
        nslides = n // 4 + (1 if n % 4 != 0 else 0)

        allprods.append([prods, range(nslides), nslides])

    return render(request, 'shop/index.html', {'allprods': allprods})


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')

        contact_obj = Contact(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        contact_obj.save()

    return render(request, 'shop/contact.html')


def tracker(request):
    order = None
    order_items = []
    updates = []
    message = ""

    if request.method == "POST":
        order_id = request.POST.get("order_id", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()

        if not order_id:
            message = "Order ID likho."
        else:
            try:
                order = Orders.objects.get(order_id=order_id)
            except Orders.DoesNotExist:
                message = "Koi order nahi mila."
                return render(request, "shop/tracker.html", {"message": message})

            if email and order.email != email:
                message = "Email match nahi hua."
                order = None
            elif phone and order.phone != phone:
                message = "Phone match nahi hua."
                order = None
            else:
                items = order.items_json
                if isinstance(items, str):
                    try:
                        items = json.loads(items)
                    except:
                        items = {}

                for key, item in items.items():
                    order_items.append({
                        "name": item.get("name", key),
                        "qty": item.get("qty", 0),
                        "price": item.get("price", 0),
                        "image": item.get("image", ""),
                        "url": item.get("url", "")
                    })

                updates = order.updates.order_by("-timestamp")

    return render(request, "shop/tracker.html", {
        "order": order,
        "order_items": order_items,
        "updates": updates,
        "message": message
    })


def search(request):
    return render(request, 'shop/search.html')


def product_view(request, id):
    product = Product.objects.filter(product_id=id)
    if not product:
        return render(request, 'shop/productview.html', {'product': None})
    return render(request, 'shop/productview.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get("items_json", "{}")
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        address = request.POST.get("address", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zip_code = request.POST.get("zip_code", "")

        try:
            items = json.loads(items_json)
        except:
            items = {}

        total_amount = 0
        for key, item in items.items():
            qty = int(item.get("qty", 0))
            price = int(item.get("price", 0))
            total_amount += qty * price

        order = Orders.objects.create(
            items_json=items,
            name=name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            total_amount=total_amount
        )

        OrderUpdate.objects.create(
            order=order,
            update_desc="Order placed"
        )

        request.session["order_id"] = order.order_id
        return redirect("checkout_success")

    return render(request, "shop/checkout.html")


def checkout_success(request):
    order_id = request.session.get("order_id")
    return render(request, "shop/checkout_success.html", {"order_id": order_id})


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm_password", "")

        if not username or not password:
            messages.error(request, "Username aur password required hain.")
            return render(request, "shop/signup.html")

        if password != confirm:
            messages.error(request, "Password match nahi hua.")
            return render(request, "shop/signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ye username already exist karta hai.")
            return render(request, "shop/signup.html")

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("/shop/")

    return render(request, "shop/signup.html")

def login_view(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/shop/")
        else:
            error = "Invalid username or password."

    return render(request, "shop/login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("login")


from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin(request):
    # ⚡ पुराना user delete कर
    User.objects.filter(username='ajay').delete()

    # ✅ नया user सही तरीके से बना
    user = User(username='ajay', email='test@test.com')
    user.set_password('1234')   # ⚡ MUST
    user.is_staff = True
    user.is_superuser = True
    user.save()

    return HttpResponse("Admin reset created")