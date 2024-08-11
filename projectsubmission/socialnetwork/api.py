from django.db.models import Q
import pdb
from fame.models import Fame, ExpertiseAreas, FameLevels,FameUsers
from socialnetwork.models import Posts, SocialNetworkUsers
from fame.models import Fame
from django.contrib.auth import logout
# general methods independent of html and REST views
# should be used by REST and html views


def _get_social_network_user(user) -> SocialNetworkUsers:
    """Given a FameUser, gets the social network user from the request. Assumes that the user is authenticated."""
    try:
        user = SocialNetworkUsers.objects.get(id=user.id)
    except SocialNetworkUsers.DoesNotExist:
        raise PermissionError("User does not exist")
    return user


def timeline(user: SocialNetworkUsers, start: int = 0, end: int = None, published=True):
    """Get the timeline of the user. Assumes that the user is authenticated."""
    _follows = user.follows.all()
    posts = Posts.objects.filter(
        (Q(author__in=_follows) & Q(published=published)) | Q(author=user)
    ).order_by("-submitted")
    if end is None:
        return posts[start:]
    else:
        return posts[start : end + 1]


def search(keyword: str, start: int = 0, end: int = None, published=True):
    """Search for all posts in the system containing the keyword. Assumes that all posts are public"""
    posts = Posts.objects.filter(
        Q(content__icontains=keyword)
        | Q(author__email__icontains=keyword)
        | Q(author__first_name__icontains=keyword)
        | Q(author__last_name__icontains=keyword),
        published=published,
    ).order_by("-submitted")
    if end is None:
        return posts[start:]
    else:
        return posts[start : end + 1]


def follows(user: SocialNetworkUsers, start: int = 0, end: int = None):
    """Get the users followed by this user. Assumes that the user is authenticated."""
    _follows = user.follows.all()
    if end is None:
        return _follows[start:]
    else:
        return _follows[start : end + 1]


def followers(user: SocialNetworkUsers, start: int = 0, end: int = None):
    """Get the followers of this user. Assumes that the user is authenticated."""
    _followers = user.followed_by.all()
    if end is None:
        return _followers[start:]
    else:
        return _followers[start : end + 1]


def follow(user: SocialNetworkUsers, user_to_follow: SocialNetworkUsers):
    """Follow a user. Assumes that the user is authenticated. If user already follows the user, signal that."""
    if user_to_follow in user.follows.all():
        return {"followed": False}
    user.follows.add(user_to_follow)
    user.save()
    return {"followed": True}


def unfollow(user: SocialNetworkUsers, user_to_unfollow: SocialNetworkUsers):
    """Unfollow a user. Assumes that the user is authenticated. If user does not follow the user anyway, signal that."""
    if user_to_unfollow not in user.follows.all():
        return {"unfollowed": False}
    user.follows.remove(user_to_unfollow)
    user.save()
    return {"unfollowed": True}


def submit_post(
    user: SocialNetworkUsers,
    content: str,
    cites: Posts = None,
    replies_to: Posts = None,
):
    """Submit a post for publication. Assumes that the user is authenticated.
    returns a tuple of three elements:
    1. a dictionary with the keys "published" and "id" (the id of the post)
    2. a list of dictionaries containing the expertise areas and their truth ratings
    3. a boolean indicating whether the user was banned and logged out and should be redirected to the login page
    """

    # create post instance:
    post = Posts.objects.create(
        content=content,
        author=user,
        cites=cites,
        replies_to=replies_to,
    )

    # classify the content into expertise areas:
    # only publish the post if none of the expertise areas contains bullshit:
    _at_least_one_expertise_area_contains_bullshit, _expertise_areas = (
        post.determine_expertise_areas_and_truth_ratings()
    )
    
    redirect_to_logout = False

    user_fame_entries = Fame.objects.filter(user=user)
    negative_expertise_areas = {entry.expertise_area for entry in user_fame_entries if entry.fame_level.name in ["Bullshitter", "Confuser", "Botcher"]}

    post_expertise_areas = {area['expertise_area'] for area in _expertise_areas}

    post.published = not (negative_expertise_areas & post_expertise_areas) and not _at_least_one_expertise_area_contains_bullshit

    if _at_least_one_expertise_area_contains_bullshit:
        for area in _expertise_areas:
            expertise_area_object = area.get('expertise_area')
            truth_rating = area.get('truth_rating')

            
            if truth_rating and truth_rating.numeric_value < 0:
                try:
                    fame_entry = Fame.objects.get(user=user, expertise_area=expertise_area_object)
                    new_fame_level = FameLevels.objects.filter(
                        numeric_value__lt=fame_entry.fame_level.numeric_value
                    ).order_by('-numeric_value').first()

                    if new_fame_level:
                            fame_entry.fame_level = new_fame_level
                            fame_entry.save()
                    else:
                         user.is_active = False
                         user.save()
                         post.published = False  
                         redirect_to_logout = True
                         Posts.objects.filter(author=user).update(published=False)   
                    break
                except Fame.DoesNotExist:
                    confuser_fame_level = FameLevels.objects.filter(name="Confuser").first()
                if confuser_fame_level:
                    Fame.objects.create(user=user, expertise_area=expertise_area_object, fame_level=confuser_fame_level) 
                    
    post.save()

    return (
        {"published": post.published, "id": post.id},
        _expertise_areas,
        redirect_to_logout,
    )



def rate_post(
    user: SocialNetworkUsers, post: Posts, rating_type: str, rating_score: int
):
    """Rate a post. Assumes that the user is authenticated. If user already rated the post with the given rating_type,
    update that rating score."""
    user_rating = None
    try:
        user_rating = user.userratings_set.get(post=post, rating_type=rating_type)
    except user.userratings_set.model.DoesNotExist:
        pass

    if user == post.author:
        raise PermissionError(
            "User is the author of the post. You cannot rate your own post."
        )

    if user_rating is not None:
        # update the existing rating:
        user_rating.rating_score = rating_score
        user_rating.save()
        return {"rated": True, "type": "update"}
    else:
        # create a new rating:
        user.userratings_set.add(
            post,
            through_defaults={"rating_type": rating_type, "rating_score": rating_score},
        )
        user.save()
        return {"rated": True, "type": "new"}


def fame(user: SocialNetworkUsers):
    """Get the fame of a user. Assumes that the user is authenticated."""
    try:
        user = SocialNetworkUsers.objects.get(id=user.id)
    except SocialNetworkUsers.DoesNotExist:
        raise ValueError("User does not exist")

    return user, Fame.objects.filter(user=user)




def experts():
    res = {}
    for ea in ExpertiseAreas.objects.all():
        experts_list = []
        for fame in Fame.objects.filter(expertise_area=ea, fame_level__numeric_value__gt=0).order_by('-fame_level__numeric_value', '-user__date_joined'):
            experts_list.append({
                "user": fame.user,
                "fame_level_numeric": fame.fame_level.numeric_value
            })
        if experts_list:
            res[ea] = experts_list
    return res


def bullshitters():
    res = {}
    for ea in ExpertiseAreas.objects.all():
        bullshitters_list = []
        for fame in Fame.objects.filter(expertise_area=ea, fame_level__numeric_value__lt=0).order_by('fame_level__numeric_value', '-user__date_joined'):
            bullshitters_list.append({
                "user": fame.user,
                "fame_level_numeric": fame.fame_level.numeric_value
            })
        if bullshitters_list:
            res[ea] = bullshitters_list
    return res

