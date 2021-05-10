from django.shortcuts import render,redirect,get_list_or_404
from .models import Profile
from article.models import Article
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import EditProfile,EditUser,UserCreationForm
from django.contrib import messages
#UserCreationForm
# Create your views here.

def profile(request,slug):
    template='profiles/profile.html'
    profile = Profile.objects.get(slug=slug)
    articles = Article.objects.filter(auth=profile).order_by('-created')
    if request.user != profile.user and profile.author==False:
        return redirect('/')
    if profile.author==False:
        template='profiles/profileUser.html'
    context = {
        'title':'profile',
        'profile': profile,
        'articles':articles,
    }
    return render(request,template , context)


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            newuser=form.save(commit=False)
            newuser.set_password(form.cleaned_data['password'])
            newuser.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'],)
            
            login(request, user)
            messages.success(request, f'Welcome {request.user} 🥳')
            return redirect('/')

    else:
        form = UserCreationForm()
    context = {
        'title': 'Register',
        'form': form,
    }
    return render(request, 'profiles/register.html', context)


def authentication(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user)
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    context = {
        'title': 'Login',
        'form': form,
    }
    return render(request, 'profiles/login.html', context)


def editProfile(request):
    profile = Profile.objects.get(user=request.user)
    formProfile = EditProfile(request.POST or None,request.FILES or None, instance=profile)
    formUser = EditUser(request.POST or None, request.FILES or None, instance=request.user,request=request)
    if request.method == 'POST':
        if formProfile.is_valid() and formUser.is_valid():
            formProfile.save()
            formUser.save()
    if 'deleteForm' in request.POST:
        request.user.delete()
        return redirect('/')
    context = {
        'title': 'Edit Profile',
        'formProfile': formProfile,
        'formUser':formUser,
        'profile':profile,
    }
    return render(request, 'profiles/editProfile.html', context)



def vlogout(request):
    logout(request)
    context = {
        'title': 'logout',
    }
    return render(request, 'profiles/logout.html', context)


