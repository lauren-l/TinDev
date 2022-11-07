from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView

# Create your views here.
class HomeView(ListView):
    template_name = 'index.html'
