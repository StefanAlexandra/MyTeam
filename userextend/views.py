from django.shortcuts import redirect
from django.views.generic import CreateView
from userextend.forms import ManagerSignUpForm


class ManagerSignUpView(CreateView):
    template_name = 'userextend/manager_sign_up.html'
    form_class = ManagerSignUpForm

    def form_valid(self, form):
        form.instance.is_manager = True
        user = form.save()
        user.save()
        return redirect('login')
