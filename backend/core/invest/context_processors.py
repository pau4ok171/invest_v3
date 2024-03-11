from .forms import CustomAuthForm, CustomUserCreationForm


def get_context_data(request):
    context = {
        'login_form': CustomAuthForm,
        'registration_form': CustomUserCreationForm,
    }
    return context
