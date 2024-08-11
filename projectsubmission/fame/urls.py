from django.urls import path

from fame.views.html import fame_list, show_experts, show_bullshitters
from fame.views.rest import ExpertiseAreasApiView, FameUsersApiView, FameListApiView

app_name = "fame"

urlpatterns = [
    path(
        "api/expertise_areas", ExpertiseAreasApiView.as_view(), name="expertise_areas"
    ),
    path("api/users", FameUsersApiView.as_view(), name="fame_users"),
    path("api/fame", FameListApiView.as_view(), name="fame_fulllist"),
    path("html/experts", show_experts, name="experts"),
    path("html/bullshitters", show_bullshitters, name="bullshitters"),
    path("html/fame", fame_list, name="fame_list"),
]
