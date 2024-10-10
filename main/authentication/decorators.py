from django.shortcuts import redirect

def login_not_required(function=None, redirect_url='/'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    return decorator(function) if function else decorator
