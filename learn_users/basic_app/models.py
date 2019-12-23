from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):

	# create relationship
	# User has first_name, last_name, email, password, username
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	# add additional attributes
	portfolio_site = models.URLField(blank=True)
	profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
	# uploaded pic will stored in media/profile_pics

	def __str__(self):
		# Built-in attribute of django.creontrib.auth.models.User !
		return self.user.username




















