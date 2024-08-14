from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, View

from product.models import Product, Category


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        queryset = Product.objects.all()
        context = super(HomeView,self).get_context_data(**kwargs)
        context['object_list'] = queryset.filter(is_public=True)
        context['offer'] = queryset.filter(is_public=True).order_by('-discount')[:2]
        context['categories'] = Category.objects.all().order_by('title')
        context['feature_product'] = queryset.filter(is_public=False).order_by('-updated_at','-created_at')[:4]

        return context