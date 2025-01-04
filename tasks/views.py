from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin  #<- dekorator

from .forms import TaskForm
from .models import Task, Category


# Create your views here.

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'


    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)# filtruje zad tak aby wyswietlaćtylko te do zal. uzytkow.
        status = self.request.GET.get('status')#pobiera parametr status z zapytania get
        category = self.request.GET.get('category')#pobiera parametr category z zapytania GET

        if status:
            queryset = queryset.filter(status=status)
        if category:
            queryset = queryset.filter(category__name=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context



class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user # przypisanie do nowego zadania uzytkownika, ktory jest akt.zalogowany
        return super().form_valid(form) # zapisuje zadanie i przekierowuje uzytkownika na strone succes_url


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')


class TaskDeleteView(DeleteView):   #ten widok będzie usuwal obiekty modelu task
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task_list')


#Rejestracja użytkownika
class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
