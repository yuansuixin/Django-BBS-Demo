from django.core import cache
from django.shortcuts import render, redirect

# Create your views here.
from math import ceil

from myapp.models import Articles


def post_list(request):
    '''
    首页帖子列表,自定义页码
    :param request:
    :return:
    '''
    # posts = Post.objects.all()
    page = int(request.GET.get('page', 1))
    total = Articles.objects.count()
    pages = ceil(total / 5)  # 总页数

    start = (page - 1) * 5
    end = start + 5
    # 按照时间顺序排序，最早发布的在最前面
    posts = Articles.objects.all().order_by('-id')[start:end]

    return render(request, 'post_list.html',
                  {'posts': posts, 'pages': range(1, pages + 1)})


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Articles.objects.create(title=title, content=content)
        return redirect('/read/?post_id=%s' % post.id)
    else:
        return render(request, 'create.html')

def read(request):
    post_id = int(request.GET.get('post_id', 1))
    # 从缓存中获取
    key = 'Post-%s'% post_id
    post = cache.get(key)
    if post is None:
        # 如果缓存中没有，从数据库中获取，同时添加到缓存
        post = Articles.objects.get(id=post_id)
        cache.set(key,post)

    print('************************888')
    return render(request, 'read.html', {'post': post})


def edit(request):
    if request.method == 'POST':
        # 取出 post
        post_id = int(request.POST.get('post_id', 1))
        print(post_id)
        post = Articles.objects.get(id=post_id)
        # 更新数据
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        # 添加到缓存
        key = 'Post-%s' % post_id
        cache.set(key,post)
        return redirect('/read/?post_id=%s' % post.id)
    else:
        post_id = int(request.GET.get('post_id', 1))
        post = Articles.objects.get(id=post_id)
        return render(request, 'edit.html', {'post': post})


def search(request):
    keyword = request.POST.get('keyword')
    print('******777*********',keyword)
    posts = Articles.objects.filter(content__contains=keyword)
    return render(request, 'search.html', {'posts': posts})




