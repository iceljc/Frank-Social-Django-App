from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
	return render(request, 'basic_app/index.html')


@login_required
def special(request):
	return HttpResponse("You are logged in. Nice!")


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))



def register(request):
	registered = False

	if request.method == 'POST':
		# Get info from "both" forms
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileInfoForm(data=request.POST)

		# Check to see both forms are valid
		if user_form.is_valid() and profile_form.is_valid():
			# Save User Form to Database
			user = user_form.save()
			# hash password
			user.set_password(user.password)
			# Update with Hashed password
			user.save()

			# deal with extra info
			# commit=False, not save to database directly
			profile = profile_form.save(commit=False)
			profile.user = user

			if 'profile_pic' in request.FILES:
				profile.profile_pic = request.FILES['profile_pic']

			# now save profile to db
			profile.save()
			registered = True
		else:
			# One of the forms was invalid if this else gets called
			print(user_form.errors, profile_form.errors)
	else:
		# Was not an HTTP post so we just render the forms as blank.
		user_form = UserForm()
		profile_form = UserProfileInfoForm()


	return render(request, 'basic_app/registration.html', 
		{
			'user_form': user_form,
			'profile_form': profile_form,
			'registered': registered
		})




def user_login(request):

	if request.method == 'POST':
		# First get the username and password
		username = request.POST.get('username')
		password = request.POST.get('password')

		# Django's built-in authentication function
		user = authenticate(username=username, password=password)

		if user:
			# Check it the account is active
			if user.is_active:
				# Log the user in.
				login(request, user)
				# redirect the user back to some page.
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your account is not active.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return HttpResponse("Invalid login details supplied.")

	else:
		# Nothing has been provided for username or password.
		return render(request, 'basic_app/login.html', {})

















