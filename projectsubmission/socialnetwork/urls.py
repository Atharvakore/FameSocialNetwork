from django.urls import path

from socialnetwork.views.html import timeline, follow, unfollow
from socialnetwork.views.rest import PostsListApiView

app_name = "socialnetwork"

urlpatterns = [
    path("api/posts", PostsListApiView.as_view(), name="posts_fulllist"),
    path("html/timeline", timeline, name="timeline"),
    path("html/follow", follow, name="follow"),
    path("html/unfollow", unfollow, name="unfollow"),
]
