from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from  django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    return HttpResponse('Это ответ на первый запрос')


def hello(request):
    return HttpResponse('Hello world!')

def post_list(request):
    posts_list = Post.objects.filter(status=Post.Status.PUBLISHED).all()
    paginator = Paginator(posts_list,2)
    pagw_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(pagw_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'blog/posts/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, publish__year = year, publish__month = month,
                             publish__day = day, slug = post)
    return render(request, 'blog/posts/detail.html', {'post': post})