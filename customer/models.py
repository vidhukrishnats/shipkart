from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(auto_now_add=True, null=True)
    is_admin = models.BooleanField(default=False, null=True)
    is_staff = models.BooleanField(default=False, null=True)
    is_active = models.BooleanField(default=False, null=True)
    is_superadmin = models.BooleanField(default=False, null=True)
    is_email_verified = models.BooleanField(default=False, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name    

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    cat_image = models.ImageField(upload_to='images/', null=True)
    class Meta:
        verbose_name_plural = 'categories'
    def get_absolute_url(self):
        return reverse('category_list', args=[self.slug])
    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    colour = models.CharField(max_length=20, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='product_creator')
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255)
    in_stock = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created', '-updated')
    def get_absolute_url(self):
        return reverse('product', args=[self.slug])
    def __str__(self):
        return self.title


