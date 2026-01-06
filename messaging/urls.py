from django.urls import path

from . import views

app_name = "messaging"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("start/<int:user_id>/", views.start_conversation, name="start"),
    path("conversation/<int:pk>/", views.conversation_detail, name="conversation"),
    path(
        "conversation/<int:pk>/messages/",
        views.conversation_messages_partial,
        name="messages_partial",
    ),
]
