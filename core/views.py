from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, DeleteView, UpdateView, CreateView
from .models import Charity, LOCATION, FOR_WHO, PURPOSE, GENDER, AGE, BOOKS, Help, Clothes, Toys, Books, Others, \
    Bags, Address, Donate
from .forms import LoginForm, SignUpForm, SetAdminPermissionForm, AddAdminForm, AddCharityForm, ModifyProfileForm, \
    ChangePasswordForm
from .utils import get_things
import json
from dateutil.parser import parse
import datetime


class LandingPage(View):

    def get(self, request):
        donates = Donate.objects.filter(user_id=request.user.id)
        context = {}
        total_bags = 0
        total_donate = len(donates)
        total_charity = []
        for donate in donates:
            total_bags += int(donate.bags.number_of_bags)
            if donate.charity.charity_name not in total_charity:
                total_charity.append(donate.charity.charity_name)
        context['total_bags'] = total_bags
        context['total_donate'] = total_donate
        context['total_charity'] = len(total_charity)
        return render(request, 'index.html', {'context': context})


class LoginView(FormView):

    template_name = 'registration/login2.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        next_page = self.request.GET.get('next')
        try:
            u = User.objects.get(email=email)
        except Exception:
            msg = 'Nie ma takiego użytkownika'
            return render(self.request, 'registration/login2.html', {'form': form, 'msg': msg})
        user = authenticate(username=u.username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('/')
            else:
                msg = 'Użytkownik jest nieaktywny. Skontaktuj się z administratorem'
                return render(self.request, 'registration/login2.html', {'form': form, 'msg': msg})
        else:
            msg = "Błędne hasło lub email"
            return render(self.request, 'registration/login2.html', {'form': form, 'msg': msg})

    def form_invalid(self, form):
        msg = "Niepoprawne dane"
        return render(self.request, 'registration/login2.html', {'form': form, 'msg': msg})


class SignUpView(FormView):

    form_class = SignUpForm
    success_url = reverse_lazy('landing_page')
    template_name = 'register.html'

    def form_valid(self, form):
        if form.cleaned_data['password1'] == form.cleaned_data['password2']:
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    password=form.cleaned_data['password1'],
                    email=form.cleaned_data['email'],
                )
                user_group = Group.objects.get(name='Użytkownik')
                user_group.user_set.add(user)
                return redirect('landing_page')
            except Exception:
                msg = 'Taki użytkownik już istnieje'
                return render(self.request, 'register.html', {'form': form, 'msg': msg})
        else:
            msg = 'Hasła są niezgodne'
            return render(self.request, 'register.html', {'form': form, 'msg': msg})


class AdminListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'User.add_permission'
    login_url = '/login'

    def get(self, request):
        admins = User.objects.filter(groups__name='Administrator')
        return render(request, 'adminList.html', {'admins': admins})


class SetAdminPermission(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = 'User.add_permission'
    login_url = '/login'
    form_class = SetAdminPermissionForm
    template_name = 'SetAdminPermission.html'

    def form_valid(self, form):
        username = form.cleaned_data['user']
        user = User.objects.get(username=username[0])
        group_admin = Group.objects.get(name='Administrator')
        group_admin.user_set.add(user)  # Dodaje obiekt User do grupy administrator
        if user.groups.filter(name='Użytkownik').exists():
            Group.objects.get(name='Użytkownik').user_set.remove(user)  # Usuwa obiekt User z grupy użytkownik
        return redirect('admin_list')


class AddAdminView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    login_url = 'login'
    permission_required = 'User.add_user'
    form_class = AddAdminForm
    #TODO: Does this view is really need?


class DeleteUserView(DeleteView):
    model = User
    success_url = '/admin-list'


class ModifyUserView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name_suffix = '_update_form'
    success_url = '/admin-list'
    #todo: zalinkować przycisk dodaj administratora


class CharityListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Charity
    fields = '__all__'
    ordering = ['id']


class CharityAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    permission_required = 'Charity.add_charity'
    model = Charity
    form_class = AddCharityForm
    success_url = 'charity-list'


class CharityUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'login'
    permission_required = 'Charity.change_charity'
    model = Charity
    form_class = AddCharityForm
    template_name_suffix = '_update_form'
    success_url = '/charity-list'


class CharityDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = 'login'
    permission_required = 'Charity.delete_charity'
    model = Charity
    success_url = reverse_lazy('charity_list')


class UserProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login2')

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        return render(request, 'UserProfile.html', {'user': user})


class UserProfileModifyView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login2')

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        form = ModifyProfileForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })
        return render(request, 'auth/user_form.html', {'form': form})

    def post(self, request, pk):
        form = ModifyProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=pk)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            return redirect(f'/user/profile/{user.pk}')
        else:
            msg = 'Niepoprawne dane'
            return render(request, 'auth/user_form.html', {'form': form, 'msg': msg})


class ChangePasswordView(LoginRequiredMixin, View):

    login_url = reverse_lazy('login2')

    def get(self, request):
        form = ChangePasswordForm
        return render(request, 'auth/user_change_password.html', {'form': form})

    def post(self, request):
        pk = request.POST['pk']
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            u = User.objects.get(pk=pk)
            password = form.cleaned_data['password']
            user = authenticate(username=u.username, password=password)
            if user is not None:
                if form.cleaned_data['new_password'] == form.cleaned_data['check_password']:
                    u.set_password(form.cleaned_data['new_password'])
                    u.save()
                    logout(request)
                    return redirect('login2')
                else:
                    return render(request, 'auth/user_change_password.html',
                                  {'form': form, 'msg': 'Hasła nie zgadzają się'})
            else:
                return render(request, 'auth/user_change_password.html', {'form': form, 'msg': 'Błędne hasło'})
        else:
            msg = "Nieprawidłowe dane"
            return render(request, 'auth/user_change_password.html', {'form': form, 'msg': msg})


class FormStepOne(LoginRequiredMixin, View):

    login_url = reverse_lazy('login2')

    def get(self, request):
        locations = {}
        for item in LOCATION:
            locations[item[1]] = item[1]
        ctx = {}
        ctx['for_who'] = FOR_WHO
        ctx['purpose'] = PURPOSE
        ctx['gender'] = GENDER
        ctx['age'] = AGE
        ctx['books'] = BOOKS
        ctx['help'] = Help.objects.all()
        return render(request, 'form.html', {'ctx': ctx,
                                             'locations': locations})


def load_charity(request):

    def get_location(location):
        for item in LOCATION:
            if location in item:
                loc = item[0]
        return loc

    def get_data(queryset):
        arr = []
        for data in queryset:
            temp = {}
            help_arr = []
            temp['charity_name'] = data.charity_name
            temp['location'] = data.get_location_display()
            for helps in data.help.all():
                help_arr.append(helps.for_who)
            temp['help'] = help_arr
            arr.append(temp)
        if arr[0]:
            return json.dumps(arr)
        else:
            msg = "Nie znaleziono organizacji"
            return msg

    def get_for_who(search_charity, for_who):
        search_charity_arr = []
        for item in for_who:
            temp = search_charity.filter(help__for_who=item)
            for org in temp:
                if org not in search_charity_arr:
                    search_charity_arr.append(org)
        return search_charity_arr

    location = request.GET.get('location')
    for_who = request.GET.get('for_who').split(",")
    search = request.GET.get('search')

    if len(search) > 0:
        all_charity = Charity.objects.filter(charity_name__contains=search)
        data = get_data(all_charity)
        return HttpResponse(data)

    elif (len(location) > 0 and location != '- wybierz -') and len(for_who) == 1:
        location = get_location(location)
        search_charity = Charity.objects.filter(location=location)
        data = get_data(search_charity)
        return HttpResponse(data)

    elif (len(location) > 0 and location != '- wybierz -') and len(for_who) > 1:
        location = get_location(location)
        search_charity = Charity.objects.filter(location=location)
        all_charity = get_for_who(search_charity, for_who)
        data = get_data(all_charity)
        return HttpResponse(data)

    elif location == '- wybierz -' and len(for_who) > 1:
        search_charity = Charity.objects.all()
        all_charity = get_for_who(search_charity, for_who)
        data = get_data(all_charity)
        return HttpResponse(data)

    else:
        return HttpResponse('Nie ma takiej organizacji')


class SaveDonateView(LoginRequiredMixin, View):

    login_url = reverse_lazy('login2')

    def get(self, request):
        bags = request.GET.get('bags')
        street = request.GET.get('street')
        city = request.GET.get('city')
        postcode = request.GET.get('postcode')
        phone = request.GET.get('phone')
        date = parse(request.GET.get('date'))
        time = request.GET.get('time')
        more_info = request.GET.get('more_info')
        forWhoSummary = request.GET.get('forWhoSummary')
        organization = request.GET.get('organization')
        things = get_things(forWhoSummary)
        """ Creating instance Clothes """
        if "clothes_type" in things:
            clothes = Clothes.objects.create(
                type=things['clothes_type'],
                for_who=things['clothes_for_who'],
                purpose=things['clothes_purpose']
            )
        else:
            clothes = None

        """ Checking if useless clothes was checked """
        if "useless_clothes" in things:
            useless_clothes = True
        else:
            useless_clothes = False

        """ Creating instance Toys """
        if 'toys' in things:
            toys = Toys.objects.create(
                toys=things['toys']
            )
        else:
            toys = None

        """ Createing instance Books """
        if 'books' in things:
            books = Books.objects.create(
                books=things['books']
            )
        else:
            books = None

        """ Creating instance Others """
        if 'others' in things:
            others = Others.objects.create(
                others=things['others']
            )
        else:
            others = None
        """ Creating instance bags """
        bags = Bags.objects.create(
            number_of_bags=bags
        )

        """ Loading from db charity """
        charity = Charity.objects.get(charity_name=organization)

        """ Creating instance Address """
        address = Address.objects.create(
            street=street,
            city=city,
            postcode=postcode,
            phone=phone,
            more_info=more_info,
            date=date,
            time=time
        )

        """ creating Donate instance """
        Donate.objects.create(
            user=User.objects.get(username=request.user.username),
            clothes=clothes,
            useless_clothes=useless_clothes,
            toys=toys,
            books=books,
            others=others,
            bags=bags,
            charity=charity,
            address=address,
        )

        return HttpResponse(forWhoSummary)


class DonateListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login2')
    model = Donate
    fields = '__all__'

    def get(self, request, pk):
        donate_list = Donate.objects.filter(
            user=User.objects.get(pk=pk)).order_by('-status', '-status_change', '-form_date')
        return render(request, 'core/donate_list.html', {'donate_list': donate_list})


class CollectDonateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        donate = Donate.objects.get(pk=pk)
        donate.status = True
        donate.status_change = datetime.datetime.now()
        donate.save()
        return redirect(f'/donate-list/{request.user.pk}')
