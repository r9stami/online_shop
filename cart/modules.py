from product.models import Product


class Cart:
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            product = Product.objects.get(pk=item['id'])
            item['product'] = product
            item['unique_id'] = self.unique_id_generator(product.id,item['color'],item['size'])
            item['total_price'] = int(item['quantity']) * int(item['price'])

            yield item

    def remove(self):
        del self.session['cart']

    def delete(self,id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def all_products(self):
        cart = self.cart.copy()
        count = 0
        for item in cart.values():
            count += item['quantity']
        return count

    def all_price(self):
        cart = self.cart.copy()
        price = 0
        for item in cart.values():
            price += int(item['price']) * int(item['quantity'])
        return price

    def unique_id_generator(self,id,color,size):
        result = f'{id}-{color}-{size}'
        return result

    def add_to_cart(self,product,quantity,color,size):
        unique = self.unique_id_generator(product.id,color,size)
        if unique not in self.cart:
            self.cart[unique] = {'quantity':0,'color':color,'size':size,'price':product.price,'id':product.id}
        self.cart[unique]['quantity'] += int(quantity)
        self.save()

    def save(self):
        self.session.modified = True
