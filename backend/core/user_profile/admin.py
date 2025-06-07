from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = (
        'display_name', 'avatar', 'locale',
        'country', 'currency', 'auth_provider', 'bio',
        'external_link', 'stock_view',
        'watchlisted_companies', 'portfolios'
    )
    filter_horizontal = ('watchlisted_companies', 'portfolios')


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_display_name', 'is_staff')
    list_select_related = ('profile',)

    def get_display_name(self, instance):
        return instance.profile.display_name if hasattr(instance, 'profile') else '-'

    get_display_name.short_description = 'Display Name'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Profile) and not instance.pk:
                instance.user = form.instance
            instance.save()
        formset.save_m2m()
        super().save_formset(request, form, formset, change)


# Отмена регистрации стандартной User модели и регистрация кастомной
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Отдельная регистрация Profile модели
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'locale', 'country', 'currency')
    list_filter = ('locale', 'country', 'currency')
    search_fields = ('user__username', 'display_name', 'user__email')
    raw_id_fields = ('user',)
    filter_horizontal = ('watchlisted_companies', 'portfolios')
