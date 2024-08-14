from django.urls import path
from product import views


app_name = 'product'
urlpatterns = [

    path('detail/<str:slug>', views.ProductDetailView.as_view(), name='product_detail'),
    path('list',views.ProductListView.as_view(), name='product_list'),
    path('search/product',views.ProductSearchView.as_view(), name='product_search'),
    path('filter/product',views.FilterProductView.as_view(), name='product_filter'),
    path('category/list/<int:pk>',views.CategoryDetailView.as_view(), name='category_detail'),
    path('like/<slug:slug>/<int:pk>',views.LikeProductView.as_view(), name='like'),
    path('like/most/product',views.MostLikedProductView.as_view(), name='like_most'),
    path('comment/create/<slug:slug>',views.CommentCreateView.as_view(), name='comment_create'),



]