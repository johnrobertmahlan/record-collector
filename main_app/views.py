from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Record

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class RecordList(ListView):
    model = Record

# def records_index(request):
#     records = Record.objects.all()
#     return render(request, 'records/index.html', {'records': records})

class RecordDetail(DetailView):
    model = Record

# def records_detail(request, record_id):
#     record = Record.objects.get(id=record_id)
#     return render(request, 'records/detail.html', {'record': record})

class RecordCreate(CreateView):
    model = Record
    fields = '__all__'

class RecordUpdate(UpdateView):
    model = Record
    fields = ['record_label', 'release_year']

class RecordDelete(DeleteView):
    model = Record
    success_url = "/records/"