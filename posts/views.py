from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *
from .models import *
from events.models import Event
from django.utils import timezone
from notify.signals import notify
from django.contrib.auth.decorators import login_required
from czaswolny.decorators import user_not_banned
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
@user_not_banned
def index(request):
    return render(request, 'posts/index.html')


@login_required
@user_not_banned
def create(request, pk):
    if request.method == "POST":
        event = get_object_or_404(Event, pk=pk)
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date = timezone.now()
            post.save()
            event.posts.add(post)
            return redirect('events:details', pk=event.pk)
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})


@login_required
@user_not_banned
def createcomment(request, pk, pk2):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.publish_date = timezone.now()
            comment.save()
            post.comments.add(comment)
            if request.user != post.author:
                notify.send(request.user, recipient=post.author, actor=request.user, verb='commented your post.', nf_type='post_commented')
            return redirect('posts:details', pk=post.pk, pk2=pk2)
    else:
        form = CommentForm()
    return render(request, 'posts/createcomment.html', {'form': form})


@login_required
@user_not_banned
def details(request, pk, pk2):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))
    if pk2 is None:
        return HttpResponseRedirect(reverse('events:index'))

    post = get_object_or_404(Post, pk=pk)
    event = get_object_or_404(Event, pk=pk2)
    comments_all = post.comments.all().order_by('-publish_date')

    # Paginacja co 5 odpowiedzi
    paginator = Paginator(comments_all, 5)
    page = request.GET.get('page', 1)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    return render(request, 'posts/details.html', {'post': post, 'event': event, 'comments': comments})


@require_POST
@login_required
@user_not_banned
def destroy(request, pk, pk2):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))
    event = get_object_or_404(Event, pk=pk2)
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return HttpResponseRedirect(reverse('events:index'))

    post.delete()
    return redirect('events:details', pk=event.pk)


@require_POST
@login_required
@user_not_banned
def destroycomment(request, pk, pk2, pk3):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))
    if pk2 is None:
        return HttpResponseRedirect(reverse('events:index'))
    event = get_object_or_404(Event, pk=pk2)
    post = get_object_or_404(Post, pk=pk)
    comment = get_object_or_404(Comment, pk=pk3)

    if request.user != comment.author:
        return HttpResponseRedirect(reverse('events:index'))

    comment.delete()
    return redirect('posts:details', pk=post.pk, pk2=event.pk)


@require_POST
@login_required
@user_not_banned
def like(request, pk, pk2):
    if pk is None:
        return HttpResponseRedirect(reverse('posts:index'))

    post = get_object_or_404(Post, pk=pk)
    event = get_object_or_404(Event, pk=pk2)
    comments = post.comments.all()
    post.likes.add(request.user)

    return render(request, 'posts/details.html', {'post': post, 'event': event, 'comments': comments})


@require_POST
@login_required
@user_not_banned
def unlike(request, pk, pk2):
    if pk is None:
        return HttpResponseRedirect(reverse('events:index'))

    post = get_object_or_404(Post, pk=pk)
    event = get_object_or_404(Event, pk=pk2)
    comments = post.comments.all()
    post.likes.remove(request.user)

    return render(request, 'posts/details.html', {'post': post, 'event': event, 'comments': comments})
