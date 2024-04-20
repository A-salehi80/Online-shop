from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserRegBase
from django.contrib.auth import login
from django.contrib import messages


def register(request):

	if request.method != 'POST':
		form = UserCreationForm()
	else:
		form = UserCreationForm(data=request.POST)
		if form.is_valid():
			new_user = form.save()
			login(request, new_user)
			return redirect('main:index')

	context = {'form': form}
	return render(request, 'registration/registeration.html', context)

