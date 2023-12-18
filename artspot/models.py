from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.utils import timezone
import datetime
timezone.now()

#Marketplace
class Artwork(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    artist = models.CharField(max_length=50, null=False, blank=False)
    length = models.PositiveIntegerField(db_column='length')
    width = models.PositiveIntegerField(db_column='widht')
    category = models.CharField(max_length=50, null=False, blank=False)
    medium = models.CharField(max_length=50, null=False, blank=False)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

#Marketplace: Category
class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    def __str__(self):
        return self.name

#Marketplace: Type of Artwork
class Medium(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    def __str__(self):
        return self.name

#Marketplace: Customer
class Customer(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=15, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=50, null=False, blank=False)
        
    def __str__(self):
        return f'{self.first_name}{self.last_name}'

#Marketplace: Product
class Product(models.Model):
        name = models.CharField(max_length=50, null=False, blank=False)
        artist = models.CharField(max_length=50, null=False, blank=False)
        length = models.PositiveIntegerField(db_column='length', default=0)
        width = models.PositiveIntegerField(db_column='width')
        medium = models.ForeignKey(Medium, on_delete=models.CASCADE, default=1)
        category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
        description = models.CharField(max_length=250, default='', null=True, blank=True)
        price_amount = models.DecimalField(default=0, decimal_places=2, max_digits=5)
        price_currency = models.CharField(default='EUR', max_length=3)
        image = models.ImageField(upload_to='images/userimage/')
        def __str__(self):
            return self.name

#Marketplace: Order
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    adress =  models.CharField(max_length=100, default='', null=True, blank=True)
    phone = models.CharField(max_length=20, default='',  null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product
        

#Blog

STATUS = ((0, "Draft"), (1, "Published"))
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

