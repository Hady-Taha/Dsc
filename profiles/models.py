from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    firstName=models.CharField(max_length=50, blank=True, null=True)
    lastName=models.CharField(max_length=50, blank=True, null=True)
    photo=models.ImageField(upload_to='profilePhoto',default='user.png')
    bio = models.TextField(max_length=100, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    bookmarked = models.ManyToManyField(to='article.Article')
    author = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.user))
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

    @property
    def get_all_bookmarked(self):
        return self.bookmarked.all()
    
   

