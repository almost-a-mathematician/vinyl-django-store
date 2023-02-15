from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from . funcs import cookieCart, cartData, guestOrder

from .models import *


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}

    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):     
    data = json.loads(request.body) # считывает формат джсона и возвращает питоновский обЪект
    productId = data['productId']
    action = data['action']

    print('action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    
    # print('product', product)
    print(Order.objects.filter(customer=customer))
    order = None
    if Order.objects.filter(customer=customer,complete=False).exists():
        order = Order.objects.filter(customer=customer,complete=False).first()
    else:
        order = Order.objects.create(customer=customer,complete=False)
    orderItem,created = OrderItem.objects.update_or_create(order=order, product=product)
    print("order item created",orderItem)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, complete=False).first()

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        print("if statemnet")
        order.complete = True
    order.save()
    print("complete",order.complete)

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            country=data['shipping']['country'],
            city=data['shipping']['city'],
            address=data['shipping']['address'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!', safe=False)
