from django.db import models
from profiles.models import Profile
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=150)
    cover = models.ImageField(upload_to='categoryCover', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    
    def __str__(self):
        return str(self.title)
    
    # @property
    # def get_articles(self):
    #     return self.article_set.all()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{str(self.title)}')
        super(Category, self).save(*args, **kwargs)



class Article(models.Model):
    auth = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    cover = models.ImageField(upload_to='articleCover', blank=True, null=True)
    content = RichTextUploadingField()
    like = models.ManyToManyField(Profile, related_name='articleLike', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)
    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{str(self.title)}-{self.id}')
        super(Article, self).save(*args, **kwargs)

    @property
    def get_all_like(self):
        return self.like.all()
    
    @property
    def get_all_comments(self):
        return self.comments_set.all().order_by('-created')


class Comments(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(f'{self.article.title[:5]} - {self.user}')
