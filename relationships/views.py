from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from accounts.models import User
from .models import Follow


@login_required
def follow(request, pk):
    target = get_object_or_404(User, pk=pk)
    if request.method == "POST" and target != request.user:
        Follow.objects.get_or_create(follower=request.user, following=target)
    return redirect("profiles:detail", pk=pk)


@login_required
def unfollow(request, pk):
    target = get_object_or_404(User, pk=pk)
    if request.method == "POST" and target != request.user:
        Follow.objects.filter(follower=request.user, following=target).delete()
    return redirect("profiles:detail", pk=pk)
