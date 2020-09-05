from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Record, Listening, Label
from .forms import ListeningForm

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

def records_detail(request, record_id):
    record = Record.objects.get(id=record_id)
    listening_form = ListeningForm()
    return render(request, 'records/detail.html', {'record': record, 'listening_form': listening_form})

class RecordCreate(CreateView):
    model = Record
    fields = '__all__'

class RecordUpdate(UpdateView):
    model = Record
    fields = ['name', 'artist', 'record_label', 'release_date']

class RecordDelete(DeleteView):
    model = Record
    success_url = "/records/"

def add_listening(request, record_id):
    form = ListeningForm(request.POST)

    if form.is_valid():
        new_listening = form.save(commit=False)
        new_listening.record_id = record_id
        new_listening.save()

    return redirect('records_detail', record_id=record_id)

class LabelIndex(ListView):
    model = Label

class LabelCreate(CreateView):
    model = Label
    fields = '__all__'

class LabelDetail(DetailView):
    model = Label

class LabelUpdate(UpdateView):
    model = Label
    fields = ['name']

class LabelDelete(DeleteView):
    model = Label
    success_url = '/labels/'