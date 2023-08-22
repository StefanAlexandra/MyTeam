from userextend.models import UserProfile


def profile_context(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile = None
    else:
        profile = None

    return {'profile': profile}
