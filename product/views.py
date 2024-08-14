import os

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q, Max
from django.shortcuts import render, redirect
from django.views.generic import DetailView , View
from django.http import JsonResponse


from account.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from product.models import Product, Size, Category, Like, Comment, HeadImage


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        user = User.objects.all()
        context = super(ProductDetailView , self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if self.request.user.likes.filter(product__slug=self.object.slug,user_id=self.request.user).exists():
                context['is_like'] = True
            else:
                context['is_like'] = False
        context['most_liked'] = Like.objects.all()


        return context





class ProductListView(View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.all().filter(parent=None)
        sizes = Size.objects.all()
        qs = Product.objects.filter(is_public=True)

        page = request.GET.get('page')
        paginator = Paginator(qs, 3)
        object_list = paginator.get_page(page)

        context = {
            'object_list': object_list,
            'category': category,

        }
        return render(request, 'product/product_list.html', context)


class ProductSearchView(View):
    def get(self, request):

        q = request.GET.get('q')
        search = Product.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
        page = request.GET.get('page')
        paginator = Paginator(search, 3)
        object_list = paginator.get_page(page)

        context = {
            'object_list': object_list,

        }
        return render(request,'product/product_list.html',context)


class FilterProductView(View):
    def post(self, request):
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        category = request.POST.get('category')
        print(f'{min_price} - {max_price} - {category}')
        queryset = Product.objects.filter(is_public=True)

        if category is not None:
            get_cat = Category.objects.all()
            get_cat = get_cat.get(title=category)
            queryset = get_cat.products.all()

        if min_price and max_price:
            if min_price == '':
                min_price = 0
            if max_price == '':
                max_price = queryset.all().aggregate(Max('price'))
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
        context = {
            'object_list': queryset,
        }
        return render(request,'product/product_list.html',context)


class CategoryDetailView(View):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        product = category.products.all()[:4]
        return render(request,'product/product_list.html',{'object_list':product})


class MostLikedProductView(LoginRequiredMixin,View):
    def get(self, request):
        likes = Product.objects.all().filter(likes__in=Like.objects.filter(user_id=request.user.id))[:3]

        return render(request,'product/product_list.html',{'object_list':likes})


class LikeProductView(LoginRequiredMixin,View):
    def get(self, request, slug,pk):
         try:
            like = Like.objects.get(product__slug=slug,user_id=self.request.user)
            like.delete()
            return JsonResponse({'response':'unlike'})

         except:

            Like.objects.create(product_id=pk,user_id=request.user.id)
            return JsonResponse({'response':'like'})


class CommentCreateView(LoginRequiredMixin,View):
    def post(self,request,slug):

        queryset = Product.objects.get(slug=slug)
        email = request.POST.get('email')
        message = request.POST.get('message')

        Comment.objects.create(user=request.user,product=queryset,email=email,message=message)
        return redirect('product:product_detail',slug)






