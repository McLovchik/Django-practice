import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import AuthForm, ExtendedRegisterForm, EditProfileForm
from django.contrib.auth.views import LoginView, LogoutView
from .models import Profile, PersonalCabinet
from django.views import generic, View
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from app_goods.models import LoyaltyProgram, Offer
import random
import logging


logger = logging.getLogger(__name__)


class UserLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        logger.info(
            f'{datetime.datetime.now()} Пользователь {self.request.user.username} аутентифицировался.'
        )
        return self.get_redirect_url() or self.get_default_redirect_url()


class UserLogoutView(LogoutView):
    pass


def register_view(request):
    if request.method == 'POST':
        usual_users_group = Group.objects.get(name='Обычные пользователи')
        loyalty_programs = LoyaltyProgram.objects.all()
        offers = Offer.objects.all()
        form = ExtendedRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            city = form.cleaned_data.get('city')
            phone = form.cleaned_data.get('phone')
            profile = Profile(
                user=user,
                city=city,
                phone=phone,
            )
            profile.save()
            PersonalCabinet.objects.create(
                profile=profile,
                offer=random.choice(offers) if len(list(offers)) else None,
                loyalty_program_item=random.choice(loyalty_programs) if len(list(loyalty_programs)) else None
            )
            # Profile.objects.create(
            #     user=user,
            #     city=city,
            #     phone=phone,
            #     # loyalty_program_item=random.choice(loyalty_programs) if len(list(loyalty_programs)) else None
            # )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            usual_users_group.user_set.add(user)
            return redirect('/news')
    else:
        form = ExtendedRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class ProfilePageView(generic.DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user_page.html'


class UserEditFormView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        if self.request.user != user:
            return self.handle_no_permission()
        user_form = EditProfileForm(instance=user)
        return render(request, template_name='users/user_edit.html',
                      context={'user_form': user_form, 'user_id': user_id})

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_form = EditProfileForm(request.POST, instance=user)

        if user_form.is_valid():
            user.save()
            return redirect(reverse('base-page'))
        return render(request, template_name='users/user_edit.html',
                      context={'profile_form': user_form, 'user_id': user_id})


class UsersListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'app_users.can_verify_user'
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users_list'


@permission_required('app_users.can_verify_user')
def verification_user_view(request, **kwargs):
    verif_users_group = Group.objects.get(name='Верифицированные пользователи')
    user = User.objects.get(id=kwargs['pk'])
    verif_users_group.user_set.add(user)
    return redirect('/users')


# class UserPageView(generic.edit.FormMixin, generic.DetailView):
#     model = User
#     context_object_name = 'one_user'
#     template_name = 'users/user_page.html'
#     form_class = ExtendedRegisterForm


# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('/news')
#     else:
#         form = UserCreationForm()
#     return render(request, 'users/register.html', {'form': form})


# def logout_view(request):
#     logout(request)
#     return HttpResponse('Вы успешно вышли из под своей учетной записи')


# def login_view(request):
#     if request.method == 'POST':
#         auth_form = AuthForm(request.POST)
#         if auth_form.is_valid():
#             username = auth_form.cleaned_data['username']
#             password = auth_form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Вы успешно вошли в систему')
#                 else:
#                     auth_form.add_error('__all__', 'Учетная запись пользователя не активна')
#             else:
#                 auth_form.add_error('__all__', 'Проверьте правильность написания логина и пароля')
#     else:
#         auth_form = AuthForm()
#     context = {
#         'form': auth_form
#     }
#     return render(request, 'users/login.html', context=context)
