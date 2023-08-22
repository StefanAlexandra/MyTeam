from django.contrib.auth.decorators import user_passes_test


def manager_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_manager,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def member_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_member,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
