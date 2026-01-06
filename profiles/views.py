from django.contrib.auth.decorators import login_required
from django.db.models import Q, Value
from django.db.models.functions import Concat, Lower
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from relationships.models import Follow
from .forms import ProfileForm
from .models import Profile


def profile_search(request):
    query = request.GET.get("q", "").strip()
    results = []
    if query:
        normalized_query = " ".join(query.split())
        profiles_qs = Profile.objects.select_related("user")
        profiles_qs = profiles_qs.annotate(
            full_name=Concat("user__first_name", Value(" "), "user__last_name"),
            full_name_lower=Lower(
                Concat("user__first_name", Value(" "), "user__last_name"),
            ),
        ).filter(
            Q(user__first_name__icontains=normalized_query)
            | Q(user__last_name__icontains=normalized_query)
            | Q(user__email__icontains=normalized_query)
            | Q(full_name__icontains=normalized_query)
            | Q(headline__icontains=normalized_query),
        )
        if request.user.is_authenticated:
            profiles_qs = profiles_qs.exclude(user=request.user)
        results = list(profiles_qs)
    following_ids = set()
    if request.user.is_authenticated:
        following_ids = set(
            Follow.objects.filter(follower=request.user).values_list(
                "following_id",
                flat=True,
            ),
        )
    return render(
        request,
        "profiles/search.html",
        {"query": query, "results": results, "following_ids": following_ids},
    )


def profile_detail(request, pk):
    profile = get_object_or_404(Profile, user__pk=pk)
    user_posts = profile.user.posts.order_by("-created_at")
    followers_count = profile.user.followers.count()
    following_count = profile.user.following.count()
    is_following = False
    if request.user.is_authenticated and request.user != profile.user:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile.user,
        ).exists()
    context = {
        "profile": profile,
        "posts": user_posts,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
    }
    return render(request, "profiles/detail.html", context)


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profiles:detail", pk=request.user.pk)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "profiles/edit.html", {"form": form})


def profile_followers(request, pk):
    user = get_object_or_404(User, pk=pk)
    followers = Follow.objects.filter(following=user).select_related("follower")
    following_ids = set()
    if request.user.is_authenticated:
        following_ids = set(
            Follow.objects.filter(follower=request.user).values_list(
                "following_id",
                flat=True,
            ),
        )
    return render(
        request,
        "profiles/followers.html",
        {"profile_user": user, "followers": followers, "following_ids": following_ids},
    )


def profile_following(request, pk):
    user = get_object_or_404(User, pk=pk)
    following = Follow.objects.filter(follower=user).select_related("following")
    following_ids = set()
    if request.user.is_authenticated:
        following_ids = set(
            Follow.objects.filter(follower=request.user).values_list(
                "following_id",
                flat=True,
            ),
        )
    return render(
        request,
        "profiles/following.html",
        {"profile_user": user, "following": following, "following_ids": following_ids},
    )
