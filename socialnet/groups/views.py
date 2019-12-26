from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db import IntegrityError
from django.views import generic
from groups.models import Group, GroupMember
from . import models

# Create your views here.

class CreateGroup(LoginRequiredMixin, generic.CreateView):
	fields = ('name', 'description')
	model = Group
	template_name = 'groups/group_form.html'

class SingleGroup(generic.DetailView):
	context_object_name = 'group'
	model = Group
	template_name = 'groups/group_detail.html'

class ListGroups(generic.ListView):
	context_object_name = 'group_list'
	model = Group
	template_name = 'groups/group_list.html'


class JoinGroup(LoginRequiredMixin, generic.RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

	def get(self, request, *args, **kwargs):
		group = get_object_or_404(Group, slug=self.kwargs.get("slug"))

		try:
			GroupMember.objects.create(user=self.request.user, group=group)
		except IntegrityError:
			messages.warning(self.request, ("Warning, You are already a member of {}".format(group.name)))
		else:
			messages.success(self.request, "You are now a member of the {} group.".format(group.name))

		return super().get(request, *args, **kwargs)



class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

	def get(self, request, *args, **kwargs):
		try:
			membership = models.GroupMember.objects.filter(
				user=self.request.user,
				group__slug=self.kwargs.get("slug")
			).get()
		except models.GroupMember.DoesNotExist:
			messages.warning(self.request, "You can't leave this group because you aren't a member of it.")
		else:
			membership.delete()
			messages.success(self.request, "You have successfully left this group.")

		return super().get(request, *args, **kwargs)







