import uuid
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db import models
from account.models import User


class Category(models.Model):
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='subs')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/category',null=True,blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/product',null=True,blank=True)
    category = models.ManyToManyField(Category,null=True,blank=True,related_name='products')
    slug = models.SlugField(max_length=100, unique=True)
    # color = models.ManyToManyField(Color,related_name='colors',null=True,blank=True)
    # size = models.ManyToManyField(Size,related_name='sizes',null=True,blank=True)
    price = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Product,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('product:product_detail',kwargs={'slug':self.slug})


class Color(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True,related_name='colors')
    title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.product.title} - {self.title}'


class Size(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True,related_name='sizes')
    title = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.product.title} - {self.title}'


class Information(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='information')
    title = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class HeadImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='images/multiple image',null=True,blank=True)

    def __str__(self):
        return self.product.title


class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} = {self.product}'


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.phone

    class Meta:
        ordering = ['-created_at']
