from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import Post, Category, Ip, UserProfile
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404
from .forms import *
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist



def get_ip(request):
    req = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = request.META.get('REMOTE_ADDR')
    return ip


#60 - seconds
#@cache_page(60) 
def index(request):
    posts = Post.objects.all().prefetch_related('views')
    
    pag = Paginator(posts, 20)
    pg_number = request.GET.get('page')
    paginator = pag.get_page(pg_number)

    side_posts = posts.filter(views__gte=1).order_by('views')
    categories = Category.objects.all()

    return render(request, 'news/index.html', {'posts':paginator,
                                               'categories':categories,
                                               'side_posts':side_posts,
                                               'page_title':'Django-News-Personification',
                                               })


#@cache_page(60)
def single_news(request, pk):
    posts = Post.objects.all()
    categories = Category.objects.all()

    side_posts = posts.filter(views__gte=1).order_by('views')
    single_post = get_object_or_404(posts, pk=pk)

    comments = single_post.comments.filter(active=True)
    new_comment = False

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = single_post
            try: 
                new_comment.name = UserProfile.objects.get(user=request.user)
            except ObjectDoesNotExist:
                new_comment.name = UserProfile.objects.create(user=request.user)
    
            new_comment.save()
    else:
        comment_form = CommentForm()

    ip = get_ip(request)
    if Ip.objects.filter(ip=ip).exists():
        single_post.views.add(Ip.objects.get(ip=ip))
    else:
        Ip.objects.create(ip=ip)
        single_post.views.add(Ip.objects.get(ip=ip))
    

    return render(request, 'news/single_news.html', {'single_post':single_post, 
                                                     'categories':categories, 
                                                     'side_posts':side_posts,
                                                     'comments':comments,
                                                     'new_comment':new_comment,
                                                     'comment_form':comment_form,
                                                    })
#@cache_page(120)
def category_news(request, slug):
    posts = Post.objects.all().select_related('category')
    category_posts = posts.filter(category__category_name=slug)
    categories = Category.objects.all()
    side_posts = posts.filter(views__gte=1).order_by('views')

    pag = Paginator(category_posts, 20)
    pg_number = request.GET.get('page')
    paginator = pag.get_page(pg_number)

    if not category_posts:
        raise Http404('Category as empty')
    return render(request, 'news/index.html', {'posts':paginator,
                                               'categories':categories,
                                               'side_posts':side_posts,
                                               'page_title':slug,
                                               })

def search_news(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        searched = request.POST.get('searched')
        posts = Post.objects.filter(title__contains=searched)
        return render(request, 'news/search_news.html', {'searched':searched,
                                                         'posts':posts,
                                                         'categories':categories,
                                                         })
    else:
        return render(request, 'news/search_news.html')


def news_login(request):
    form = LoginForm()
    categories = Category.objects.all()
    msg = []
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                msg = 'Something is entered incorrectly'

        else:
            msg = 'Form is not valid'
    
    return render(request, 'news/news_login.html', {'form':form,
                                                    'msg':msg,
                                                    'categories':categories,
                                                    'title':'Login',
                                                    })

@login_required()
def news_logout(request):
    logout(request,)
    return redirect('news_login')


def news_register(request):
    form = RegisterForm()
    categories = Category.objects.all()
    msg = []
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            user = User.objects.all()
            
            if password1 != password2:
                msg = 'Passwords must be the same'

            elif user.filter(username=username):
                msg = 'Username already busy'
            
            elif user.filter(email=email):
                msg = 'This email is already registered'

            else:
                user = User.objects.create(username=username, password=make_password(password1), email=email)
                UserProfile.objects.create(user=user)
                return  redirect('home')
        else:
            msg = 'Form not valid'
                
    return render(request, 'news/news_login.html', {'form':form,
                                                    'msg':msg,
                                                    'categories':categories,
                                                    'title':'Register',
                                                    }) 

@login_required()
def create_news(request):
    categories = Category.objects.all()
    msg = ''
    form = CreateForm()
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            saved_object = form.save(commit=False)
            saved_object.user = request.user
            saved_object.save()
            return redirect('single_news', pk=saved_object.pk)
        else:
            msg = 'Form not valid'
            
            
    return render(request, 'news/create_change_news.html', {'form':form,
                                                     'categories':categories,
                                                     'msg':msg,
                                                     'title':'Create Post',
                                                     'btn':'Create',
                                                     })

#@cache_page(60)
def user_account(request, userpk):
   
    user = get_object_or_404(User, pk=userpk)
    categories = Category.objects.all()
    try:
        avatar_mod = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        avatar_mod = UserProfile.objects.create(user=request.user)
    posts = Post.objects.filter(user=user)
    comments = Comment.objects.filter(name__id=userpk).count()
    form = None
    if request.user == user:
        form = AvatarForm()
        if request.method == 'POST':
            form = AvatarForm(request.POST, request.FILES)
            if form.is_valid():
                avatar_mod.avatar = form.cleaned_data['image']
                avatar_mod.save()
                return redirect('user_account', userpk)
            
        
    return render(request, 'news/user_account.html', {'user':user,
                                                      'categories':categories,
                                                      'comments':comments,
                                                      'posts':posts,
                                                      'avatar_mod':avatar_mod,
                                                      'form':form,
                                                      })
#@cache_page(60 * 3)
def user_news(request, userpk):
    posts = Post.objects.all()
    user_news = posts.filter(user=userpk)
    pag = Paginator(user_news, 20)
    pg_number = request.GET.get('page')
    paginator = pag.get_page(pg_number)
    user = User.objects.get(pk=userpk)

    side_posts = posts.filter(views__gte=1).order_by('views')
    categories = Category.objects.all()

    return render(request, 'news/index.html', {'posts':paginator,
                                               'categories':categories,
                                               'side_posts':side_posts,
                                               'page_title':f'User - {user.username}',
                                               })

@login_required()
def change_news(request, pk):
    single_post = Post.objects.get(pk=pk)

    if request.user == single_post.user:
        categories = Category.objects.all()
        msg = ''
        form = ChangeForm(instance=single_post)

        if request.method == 'POST':
            form = ChangeForm(request.POST, instance=single_post)
            if form.is_valid():
                saved_object = form.save(commit=False)
                saved_object.save()

                return redirect('single_news', pk=saved_object.pk)
            else:
                msg = 'Form not valid'
                
                
        return render(request, 'news/create_change_news.html', {'form':form,
                                                        'categories':categories,
                                                        'msg':msg,
                                                        'title':'Change post',
                                                        'btn':'Change',
                                                        })
    else:
         raise Http404('You do not have access to this operation')


@login_required()
def delete_news(request, pk):
    categories = Category.objects.all()
    single_post = Post.objects.get(pk=pk)
    if request.user == single_post.user:
        if request.method == 'POST':
            single_post.delete()
            return redirect('home')
        else:
            return render(request,'news/confirm_delete.html', {'categories':categories})
    else:
         raise Http404('You do not have access to this operation')