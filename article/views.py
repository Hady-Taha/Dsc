from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Article, Category ,Comments
from profiles.models import Profile 
from django.db.models import Count
from django.contrib import messages
from .forms import CreateComment
# Create your views here.

def home(request):
    articles = Article.objects.all().order_by('-created')
    categories = Category.objects.all()
    topLikes = Article.objects.all().annotate(num_like=Count('like')).order_by('-num_like')[:3]
    context = {
        'title':'DCS',
        'articles':articles,
        'categories': categories,
        'topLikes': topLikes,
    }
    return render(request, 'article/home.html',context)



def article(request, slug):
    Quarticle = Article.objects.get(slug=slug)
    form = CreateComment()
    if 'addComment' in request.POST:
        form = CreateComment(request.POST)
        if form.is_valid():
            print('valid')
            form.save(commit=False)
            form.instance.user = request.user.profile
            form.instance.article = Quarticle
            form.save()
    if 'deleteComment' in request.POST:
        idCommnet = request.POST.get('deleteComment')
        comment = Comments.objects.get(id=idCommnet)
        if request.user.profile == comment.user:
            comment.delete()
    context = {
        'title': 'article',
        'article': Quarticle,
        'form':form,
        
    }
    return render(request, 'article/article.html', context)
    

def category(request, slug):
    articles = Article.objects.filter(category__slug=slug)
    topLikes = Article.objects.filter(category__slug=slug).annotate(num_like=Count('like')).order_by('-num_like')[:3]
    context = {
        'title': 'category',
        'articles': articles,
        'topLikes':topLikes,
    }
    return render(request, 'article/category.html', context)


def like(request):
    icon=None
    if request.method == 'POST':
        getArticle = Article.objects.get(id=request.POST.get('postId'))
        if request.user.profile in getArticle.like.all():
            getArticle.like.remove(request.user.profile)
            icon='far'
        else:
            getArticle.like.add(request.user.profile)
            icon = 'fa'
    context = {
        'likeNum': getArticle.get_all_like.count(),
        'icon': icon
    }
    return JsonResponse(context)


def search(request):
    if request.method == 'POST':
        articles = Article.objects.filter(title__contains=request.POST.get('searchText')).order_by('-created')
        if not articles:
            messages.warning(request, 'There are no results')
    context = {
        'articles':articles,
    }
    return render(request, 'article/titleArticle.html', context)


def saveArticle(request):
    icon=None
    if request.method == 'POST':
        getArticle = Article.objects.get(id=request.POST.get('postId'))
        getProfile = Profile.objects.get(user=request.user)
        if getArticle in getProfile.get_all_bookmarked:
            getProfile.bookmarked.remove(getArticle)
            icon='far'
        else:
            getProfile.bookmarked.add(getArticle)
            icon = 'fa'
            pass
            
    return HttpResponse(icon)
