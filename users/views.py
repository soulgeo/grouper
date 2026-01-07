from allauth.account import app_settings
from allauth.account.views import SignupView
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages

from users.models import UserProfile

from . import strings


class CustomSignupView(SignupView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['custom_message'] = strings.CALL_TO_ACTION
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        if (
            app_settings.EMAIL_VERIFICATION
            == app_settings.EmailVerificationMethod.MANDATORY
        ):
            messages.info(self.request, strings.EMAIL_VERIFY_NOTIFICATION)
        else:
            messages.success(
                self.request,
                strings.SIGNUP_SUCCESS.format(
                    first_name=form.cleaned_data['first_name']
                ),
            )
        return response


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        profile = UserProfile(user=user)
        profile.save()
        return user
