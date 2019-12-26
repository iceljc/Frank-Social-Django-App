from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify # lowercase, replace space with hash, underscore...

import misaka # a markdown parsing library
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

# This is for the in_group_members check template tag
from django import template
# used in "posts/post_list.html": get_user_groups
register = template.Library()

class Group(models.Model):
	name = models.CharField(max_length=256, unique=True)
	slug = models.SlugField(allow_unicode=True, unique=True)
	description = models.TextField(blank=True, default='')
	description_html = models.TextField(editable=False, default='', blank=True)
	members = models.ManyToManyField(User,through="GroupMember")
	
	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		self.description_html = misaka.html(self.description)
		super().save(*args, **kwargs)


	def get_absolute_url(self):
		return reverse("groups:single", kwargs={"slug": self.slug})


	class Meta:
		ordering = ["name"]



class GroupMember(models.Model):
	group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

	class Meta:
		unique_together = ("group", "user")









