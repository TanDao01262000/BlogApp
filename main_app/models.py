from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.urls import reverse

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name


class Post(models.Model):
    title = models.CharField(max_length=500, null=False, blank=False)
    content = models.CharField(max_length=50000, null=False, blank=False)
    published_date = models.DateTimeField(default=timezone.now, blank=True)
    modified_date = models.DateTimeField(default=timezone.now, blank=True)
    like_count = models.IntegerField(default=0, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        return reverse('postdetailview', kwargs={'pk':self.id})
    
    def update_like_count(self):
        self.like_count = Like.objects.filter(post=self).count()
        self.save(update_fields=['like_count'])

    def save(self, *args, **kwargs):
        self.modified_date = timezone.now()
        super(Post, self).save(*args, **kwargs)

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.id} liked {self.post}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.post.update_like_count()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.post.update_like_count()
    
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    published_date = models.DateTimeField(default=timezone.now, blank=True)
    modified_date = models.DateTimeField(default=timezone.now, blank=True)
    
    def __str__(self):
        return f"{self.user.id} has commented on {self.post.id} that {self.content}"
    
    def save(self, *args, **kwargs):
        self.modified_date = timezone.now()
        super().save(*args, **kwargs)