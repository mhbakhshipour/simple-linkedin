from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from .forms import MessageForm
from .models import Conversation, Message


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(
        Q(user1=request.user) | Q(user2=request.user),
    ).prefetch_related("messages")
    return render(request, "messaging/inbox.html", {"conversations": conversations})


def _get_or_create_conversation(user_a, user_b):
    if user_a.id > user_b.id:
        user_a, user_b = user_b, user_a
    conversation, _ = Conversation.objects.get_or_create(
        user1=user_a,
        user2=user_b,
    )
    return conversation


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.user not in conversation.participants():
        return redirect("messaging:inbox")
    if request.user == conversation.user1:
        other = conversation.user2
    else:
        other = conversation.user1
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                body=form.cleaned_data["body"],
            )
            return redirect("messaging:conversation", pk=conversation.pk)
    else:
        form = MessageForm()
    messages = conversation.messages.select_related("sender")
    return render(
        request,
        "messaging/conversation.html",
        {"conversation": conversation, "messages": messages, "form": form, "other": other},
    )


@login_required
def start_conversation(request, user_id):
    other = get_object_or_404(User, pk=user_id)
    if other == request.user:
        return redirect("messaging:inbox")
    conversation = _get_or_create_conversation(request.user, other)
    return redirect("messaging:conversation", pk=conversation.pk)


@login_required
def conversation_messages_partial(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.user not in conversation.participants():
        return redirect("messaging:inbox")
    messages = conversation.messages.select_related("sender")
    return render(
        request,
        "messaging/partials/messages_list.html",
        {"conversation": conversation, "messages": messages},
    )
