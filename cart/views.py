import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import Address
from product.models import Product
from .models import Order, OrderItem, DiscountCode
from .modules import Cart
import requests
from django.http import JsonResponse


if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

class CartDetailView(LoginRequiredMixin,View):
    def get(self, request):

        cart = Cart(request)
        return render(request , 'cart/cart.html',{'cart':cart})


class AddToCartView(View):
    def post(self, request,slug):
        if request.user.is_authenticated:
            product = Product.objects.get(slug=slug)
            quantity,color,size = request.POST.get('quantity','empty'),request.POST.get('color','empty'),request.POST.get('size','empty')
            cart = Cart(request)
            cart.add_to_cart(product,quantity,color,size)

        return redirect('cart:cart_detail')


class DeleteCartView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            cart = Cart(request)
            cart.delete(id)
            return redirect('cart:cart_detail')


class OrderDetailView(LoginRequiredMixin,View):
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        return render(request,'cart/order.html',{'order':order})


class AddOrderView(LoginRequiredMixin,View):
    def get(self, request):

        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.all_price())
        if cart.all_products == 0:
            return redirect('cart:cart_detail')
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'],
                                         quantity=item['quantity'], color=item['color']
                                         , size=item['size'], price=item['price'])
            cart.remove()
            return redirect('cart:order_detail', order.id)


class ApplyDiscountView(LoginRequiredMixin,View):
    def post(self,request,pk):

        order = Order.objects.get(id=pk)
        code = request.POST.get('discount_code')
        disc = DiscountCode.objects.get(title=code)

        if disc.quantity == 0:
            return redirect('cart:order_detail', order.id)
        order.total_price -= disc.persentage * order.total_price / 100
        disc.is_active = True
        order.save()
        disc.quantity -= 1
        disc.save()
        return redirect('cart:order_detail', order.id)


class SendRequestView(LoginRequiredMixin,View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        address = get_object_or_404(Address, id=request.POST.get("address"))
        order.address = f"{address.address} - {address.phone}"
        request.session['order_id'] = str(order.id)
        order.save()

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.total_price,
            "Description": f" {order.items.count()} عدد ",  # مطمئن شوید که متغیر description تعریف شده است
            "Phone": request.user.phone,
            "CallbackURL": settings.CALLBACK_URL,  # از settings.CALLBACK_URL استفاده کنید
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json'}

        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return redirect(ZP_API_STARTPAY + str(response['Authority']))
                else:
                    return JsonResponse({'status': False, 'code': str(response['Status'])})
            return JsonResponse({'status': False, 'code': 'unknown error'})

        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'code': 'connection error'})


class CartVerifyView(View):
    def get(self, request):
        order_id = request.session['order_id']
        order = get_object_or_404(Order, pk=int(order_id))
        authority = request.GET.get("Authority")
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.total_price,
            "Authority": authority,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                order.is_paid = True
                order.save()
                return JsonResponse({'status': True, 'RefID': response['RefID']})
            else:
                return JsonResponse({'status': False, 'code': str(response['Status'])})
        return JsonResponse({'status': False, 'error': 'Payment verification failed'})
