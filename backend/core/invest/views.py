import datetime

from dateutil.relativedelta import relativedelta
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import BaseCreateView
from django.contrib.auth.views import LoginView
from django.http.response import JsonResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from . import models
from .forms import CustomUserCreationForm

from portfolio.models import Portfolio


class HomePageView(TemplateView):
    template_name = 'invest/index.html'


class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(redirect_to=reverse_lazy('home'))

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse(data={}, status=201)
            return JsonResponse(data={'error': 'Login or password is not valid'}, status=400)
        return JsonResponse(data={'error': 'Entry login and password'}, status=400)


class RegistrationView(BaseCreateView):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(redirect_to=reverse_lazy('home'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('validate_username', None):
            return self.validate_username(request)

        # Сохранение экземпляр формы
        form = CustomUserCreationForm(request.POST)
        # Проверка валидности формы
        if form.is_valid():
            # Сохранение нового пользователя без добавления в бд
            new_user = form.save(commit=False)
            # Установка пароля
            new_user.set_password(form.cleaned_data['password1'])
            # Сохранение нового пользователя в бд
            new_user.save()
            # Авторизация пользователя
            login(self.request, new_user)
            return JsonResponse(data={'success': '201'}, status=201)
        return JsonResponse(data={'errors': form.errors}, status=400)

    def validate_username(self, request):
        username = request.POST.get('username', None)
        return JsonResponse(
            data={
                'is_taken': User.objects.filter(username__iexact=username).exists(),
                'error': 'This username is already taken'
            },
        )


class InvestCompanyListView(ListView):
    model = models.Company
    template_name = 'invest/company/list/list_v2.html'
    qs = None

    def get_queryset(self):
        self.qs = super().get_queryset()
        self.qs = self.qs.filter(is_visible=True)

        country_iso = self.kwargs.setdefault('country_iso', 'global')
        sector_slug = self.kwargs.setdefault('sector_slug', 'any')

        if country_iso != 'global':
            self.qs = self.qs.filter(country__name_iso=country_iso)
            country_name = models.Country.objects.get(name_iso=country_iso).name
            self.kwargs.__setitem__('country_name', country_name)

        if sector_slug != 'any':
            self.qs = self.qs.filter(sector__slug=sector_slug)
            sector_name = models.Sector.objects.get(slug=sector_slug).title
            self.kwargs.__setitem__('sector_name', sector_name)

        if self.qs:
            return self.qs
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['selectors_list'] = {
            'country_list': self.get_country_list(),
            'sector_list': self.get_sector_list(),
        }
        context['stock_count'] = self.get_queryset_count()
        context['last_update'] = self.last_updated()
        context['selectors'] = self.kwargs
        return context

    def get_queryset_count(self):
        return self.qs.count()

    def last_updated(self):
        return self.qs.values_list('updated').latest('updated')[0]

    def get_sector_list(self):
        country_iso = self.kwargs.get('country_iso', None)
        company_list = models.Company.objects.all().values('sector_id')

        if country_iso != 'global':
            company_list = models.Company.objects.filter(country__name_iso=country_iso).values('sector_id')

        sector_list = models.Sector.objects.filter(id__in=company_list).distinct()

        return sector_list

    def get_country_list(self):
        company_list = models.Company.objects.all().values('country_id')
        country_list = models.Country.objects.filter(id__in=company_list).distinct()

        return country_list


class InvestCompanyDetailView(DetailView):
    model = models.Company
    template_name = 'invest/company/detail/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        report = models.ReportMetadata.objects.filter(company__slug__exact=self.object.slug)
        context['report'] = report.latest('year', 'quarter') if report else None

        context['company_detail_header_info'] = self.get_company_detail_header_info()
        return context

    def get_company_detail_header_info(self):
        candles = models.CandlePerDay.objects.filter(company__slug__exact=self.object.slug)
        # currency = self.object
        # TODO: Add currency depending on Company's Country's Currency
        last_price = f'₽{candles.latest("time").close}'

        return_7d = self.get_closest_available_return(candles, days=7)
        return_1y = self.get_closest_available_return(candles, years=1)

        report = models.ReportMetadata.objects.filter(company__slug__exact=self.object.slug)
        share_outstanding = report.latest('year', 'quarter').share_outstanding if report else None

        market_cap = candles.latest("time").close * share_outstanding if share_outstanding else 'n/a'
        market_cap = self.get_humanize_money_num(market_cap)

        analyst_ideas = self.get_analyst_ideas()

        portfolios = self.get_portfolios()

        data = {
            'last_price': last_price,
            'market_cap': market_cap,
            'return_7d': return_7d,
            'return_1y': return_1y,
            'analyst_ideas': analyst_ideas,
            'portfolios': portfolios,
        }
        return data

    @staticmethod
    def get_closest_available_return(candles, **kwargs):
        last_price = candles.latest('time').close
        last_time = candles.latest('time').time
        past_time = last_time - relativedelta(**kwargs)

        past_price = candles.filter(time__lte=past_time).order_by('-time').first().close
        share_return = (last_price - past_price) / past_price * 100
        share_is_profitable = True if share_return > 0 else False

        return {'share_return': f'{share_return:.1f}%', 'is_profitable': share_is_profitable}

    def get_humanize_money_num(self, num):
        if not isinstance(num, int | float):
            return num

        for unit in ("", "t", "M", "B", "T"):
            if abs(num) < 1000.0:
                return f"₽{num:3.1f}{unit}"
            num /= 1000.0
        return f"₽{num:.1f}Q"

    def get_analyst_ideas(self):
        analyst_ideas = models.AnalystIdea.objects.filter(
            company__slug__exact=self.object.slug,
            date_target__gt=datetime.datetime.utcnow()
        )
        return analyst_ideas

    def get_portfolios(self):
        return Portfolio.objects.filter(user__exact=self.request.user)
