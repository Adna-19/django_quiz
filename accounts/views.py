from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView, View, TemplateResponseMixin
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import User, StudentProfile, TeacherProfile
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView
from .forms import (
	SignUpForm,
	StudentProfileSettingForm,
	TeacherProfileSettingForm
)

class LoginView(FormView):
	form_class = AuthenticationForm
	template_name = 'accounts/authentications/login.html'

	def form_valid(self, form):
		cd = form.cleaned_data
		user = authenticate(username=cd['username'], password=cd['password'])
		if user:
			login(self.request, user)
		return super(LoginView, self).form_valid(form)

	def get_success_url(self, **kwargs):
		if self.request.user.user_role == 'S':
			return reverse_lazy('students_dashboard')
		elif self.request.user.user_role == 'T':
			return reverse_lazy('teachers_dashboard')
		return super(LoginView, self).get_success_url(**kwargs)

class LogoutView(RedirectView):
  permanent = True
  query_string = True
  pattern_name = 'login'

  def get_redirect_url(self, *args, **kwargs):
    logout(self.request)
    return super(LogoutView, self).get_redirect_url(*args, **kwargs)

class PasswordChangeView(TemplateResponseMixin, View):
  model = User
  template_name = 'accounts/authentications/password_change_form.html'

  def get(self, request, *args, **kwargs):
    form = PasswordChangeForm(request.user)
    return self.render_to_response({'form': form})

  def post(self, request, *args, **kwargs):
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
      form.save()
      return redirect('login')

class SignUpSelectionView(TemplateView):
  template_name = 'accounts/authentications/signup_selection.html'

class SignUpView(TemplateResponseMixin, View):
	template_name = 'accounts/authentications/signup_modal_form.html'
	model = None

	def dispatch(self, request, user_role, *args, **kwargs):
		if user_role == 'S':
			self.model = StudentProfile
		elif user_role == 'T':
			self.model = TeacherProfile
		return super(SignUpView, self).dispatch(request, user_role, *args, **kwargs)

	def get(self, request, user_role, *args, **kwargs):
		form = SignUpForm()
		return self.render_to_response({'form':form, 'user_role': user_role})

	def post(self, request, user_role, *args, **kwargs):
		form = SignUpForm(request.POST)

		if form.is_valid() and not request.is_ajax():
			cd = form.cleaned_data
			user = User(
				username=cd['username'],
				email=cd['email'],
				gender=cd['gender']
			)
			user.set_password(cd['confirm_password'])
			user.user_role = user_role
			user.save()

			self.model.objects.create(user=user)
			return redirect('login')
		return self.render_to_response({'form': form})

class ProfileUpdateView(TemplateResponseMixin, View):
	template_name = 'accounts/authentications/profile_form.html'

	def get_form(self, request):
		if request.user.user_role == 'S':
			form = StudentProfileSettingForm(request.user, request.POST or None, request.FILES or None, instance=request.user.student_profile)

		elif request.user.user_role == 'T':
			form = TeacherProfileSettingForm(request.user, request.POST or None, request.FILES or None, instance=request.user.teacher_profile)

		return form

	def get(self, request, *args, **kwargs):
		form = self.get_form(request)	
		return self.render_to_response({'form': form})

	def post(self, request, *args, **kwargs):
		form = self.get_form(request)

		if form.is_valid():
			form.save()
			cd = form.cleaned_data
			request.user.username = cd['username']
			request.user.email = cd['email']
			request.user.first_name = cd['first_name']
			request.user.last_name = cd['last_name']
			request.user.gender = cd['gender']
			request.user.profile_image = cd['profile_image']
			request.user.save()

			if request.user.user_role =='S':
				return redirect('students_dashboard')
			elif request.user.user_role == 'T':
				return redirect('teachers_dashboard')
				
		return self.render_to_response({'form': form})