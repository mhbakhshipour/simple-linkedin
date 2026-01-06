from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from relationships.models import Follow
from .forms import PostForm
from .models import Post


@login_required
def feed(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(author=request.user, body=form.cleaned_data["body"])
            return redirect("posts:feed")
    else:
        form = PostForm()

    following_ids = Follow.objects.filter(
        follower=request.user,
    ).values_list("following_id", flat=True)
    posts = Post.objects.filter(
        author__in=list(following_ids) + [request.user.id],
    ).select_related("author")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    suggested_users = (
        User.objects.exclude(pk=request.user.pk)
        .order_by("-date_joined")[:5]
    )
    return render(
        request,
        "posts/feed.html",
        {"form": form, "page_obj": page_obj, "suggested_users": suggested_users},
    )


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:feed")
    else:
        form = PostForm(instance=post)
    return render(request, "posts/edit.html", {"form": form, "post": post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("posts:feed")
    return render(request, "posts/delete_confirm.html", {"post": post})
