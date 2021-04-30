from django import forms
from .models import StudentProfile, TeacherProfile, User

class BaseForm(forms.Form):
	""" ALL THE COMMON FIELDS FOR BOTH TYPE OF USERS ARE DEFINED HERE.."""
	username = forms.CharField(max_length=20)
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)
	image = forms.ImageField()
	gender = forms.ChoiceField(choices=(('M','Male'),('F', 'Female')))
	email = forms.EmailField()

	def clean_username(self):
		username = self.cleaned_data.get('username')
		alread_used_usernames = [user.username for user in User.objects.all()]
  
		if username in alread_used_usernames:
			raise forms.ValidationError("Username already in use.")
		return username

	def clean_confirm_password(self):
		passowrd1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('confirm_password')

		if passowrd1 != password2:
			raise forms.ValidationError('Mismatched Password')
		return password2


# ACTUAL PROFILE FORMS

class StudentSignUpForm(BaseForm):
  bio = forms.CharField(widget=forms.Textarea)
  password = forms.CharField(widget=forms.PasswordInput)
  confirm_password = forms.CharField(widget=forms.PasswordInput)

  def clean_username(self):
    return super(StudentSignUpForm, self).clean_username()
  
  def clean_confirm_password(self):
    return super(StudentSignUpForm, self).clean_confirm_password()

class TeacherSignUpForm(BaseForm):
	about = forms.CharField(widget=forms.Textarea)
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)

	def clean_username(self):
		return super(TeacherSignUpForm, self).clean_username()

	def clean_confirm_password(self):
		return super(TeacherSignUpForm, self).clean_confirm_password()


# REDUNDANT CODE DOWN HERE, NEEDS TO BE OPTIMIZED

class StudentProfileSettingForm(forms.ModelForm):
	username   = forms.CharField(max_length=50)
	first_name = forms.CharField(max_length=20)
	last_name  = forms.CharField(max_length=20)
	email      = forms.EmailField()

	def __init__(self, user, *args, **kwargs):
		super(StudentProfileSettingForm, self).__init__(*args, **kwargs)
		self.fields['username'].initial = user.username
		self.fields['first_name'].initial = user.first_name
		self.fields['last_name'].initial = user.last_name
		self.fields['email'].initial = user.email

	class Meta:
		model = StudentProfile
		fields = ('username', 'first_name', 'last_name', 'email', 'profile_image', 'gender', 'bio')

class TeacherProfileSettingForm(forms.ModelForm):
	username   = forms.CharField(max_length=50)
	first_name = forms.CharField(max_length=20)
	last_name  = forms.CharField(max_length=20)
	email      = forms.EmailField()

	def __init__(self, user, *args, **kwargs):
		super(TeacherProfileSettingForm, self).__init__(*args, **kwargs)
		self.fields['username'].initial = user.username
		self.fields['first_name'].initial = user.first_name
		self.fields['last_name'].initial = user.last_name
		self.fields['email'].initial = user.email

	class Meta:
		model  = TeacherProfile
		fields = ('username', 'first_name', 'last_name', 'email', 'profile_image', 'gender', 'about')
