from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from socialnetwork.models import SocialNetworkUsers

from socialnetwork import api
from socialnetwork.api import _get_social_network_user
from socialnetwork.serializers import PostsSerializer



@require_http_methods(["GET"])
@login_required
def timeline(request):
    # using the serializer to get the data, then use JSON in the template!
    # avoids having to do the same thing twice

    # get extra URL parameters:
    keyword = request.GET.get("search", "")
    published = request.GET.get("published", True)
    error = request.GET.get("error", None)

    followingsIds = []
    for following in api.follows(_get_social_network_user(request.user)):
        followingsIds.append(following.id)

    # if keyword is not empty, use search method of API:
    if keyword and keyword != "":
        context = {
            "posts": PostsSerializer(
                api.search(keyword, published=published), many=True
            ).data,
            "searchkeyword": keyword,
            "error": error,
        }
    else:  # otherwise, use timeline method of API:
        context = {
            "posts": PostsSerializer(
                api.timeline(
                    _get_social_network_user(request.user), published=published
                ),
                many=True,
            ).data,
            "searchkeyword": "",
            "error": error,
            "follows": followingsIds,
           
        }

    return render(request, "timeline.html", context=context)


@require_http_methods(["POST"])
@login_required
def follow(request):
   curr_user = _get_social_network_user(request.user)
   user_to_follow = SocialNetworkUsers.objects.get(id=request.POST.get("authorid"))
   api.follow(curr_user, user_to_follow)
   follows_user = api.follows(curr_user)
   print(follows_user)
   return redirect(reverse("socialnetwork:timeline"))



@require_http_methods(["POST"])
@login_required
def unfollow(request):
   
    curr_user = _get_social_network_user(request.user)
    user_to_unfollow = SocialNetworkUsers.objects.get(id=request.POST.get("authorid"))
    api.unfollow(curr_user, user_to_unfollow)
    return redirect(reverse("socialnetwork:timeline"))

