from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from  django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post, Comment
from .forms import CommentForm
from django.views.decorators.http import require_POST


# Create your views here.
def index(request):
    return HttpResponse('Это ответ на первый запрос')


def hello(request):
    return HttpResponse('Hello world!')

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = True
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/posts/comment.html', {'post': post, 'form': form, 'comment': comment})

class PostListView(ListView):
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED).all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/posts/list.html'

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
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'blog/posts/detail.html', {'post': post,
                                                                            'comments': comments,
                                                                            'form': form})