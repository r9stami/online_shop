from cart.modules import Cart
from cart.models import Order
from product.models import Category, Product


def category_list(request):
    categories = Category.objects.all()
    return {'category_list': categories}


def recent_product(request):
    products = Product.objects.filter(is_public=True).order_by('-updated_at','-created_at')[:8]
    return {'recent_product': products}