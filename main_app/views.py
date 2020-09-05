from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Record, Listening, Musician, Photo, User
from .forms import ListeningForm
import uuid
import boto3
from botocore.exceptions import ClientError
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

S3_BASE_URL = "https://jrm-record-collector.s3.amazonaws.com/"
BUCKET = "jrm-record-collector"

@login_required
def add_photo(request, record_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        mysession = boto3.session.Session(profile_name="record")
        s3 = mysession.client('s3')
        key = uuid.uuid4().hex[:6]  + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET,  key)
            url = f"{S3_BASE_URL}{key}"
            photo = Photo(url=url, record_id=record_id)
            photo.save()
        except ClientError as e:
            logging.error(e)
            print(e)
    return redirect('records_detail', record_id)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class RecordList(LoginRequiredMixin, ListView):
    # model = Record
    def get_queryset(self):
        queryset = Record.objects.filter(user=self.request.user)
        return queryset

# def records_index(request):
#     records = Record.objects.all()
#     return render(request, 'records/index.html', {'records': records})

@login_required
def records_detail(request, record_id):
    record = Record.objects.get(id=record_id)
    musicians_not_on_record = Musician.objects.exclude(id__in=record.musicians.all().values_list('id'))
    listening_form = ListeningForm()
    return render(request, 'records/detail.html', {'record': record, 'listening_form': listening_form, 'musicians': musicians_not_on_record})

class RecordCreate(LoginRequiredMixin, CreateView):
    model = Record
    fields = ['name', 'artist', 'record_label', 'release_date']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RecordUpdate(LoginRequiredMixin, UpdateView):
    model = Record
    fields = ['name', 'artist', 'record_label', 'release_date']

class RecordDelete(LoginRequiredMixin, DeleteView):
    model = Record
    success_url = "/records/"

@login_required
def add_listening(request, record_id):
    form = ListeningForm(request.POST)

    if form.is_valid():
        new_listening = form.save(commit=False)
        new_listening.record_id = record_id
        new_listening.save()

    return redirect('records_detail', record_id=record_id)

class MusicianIndex(LoginRequiredMixin, ListView):
    model = Musician

class MusicianCreate(LoginRequiredMixin, CreateView):
    model = Musician
    fields = '__all__'

class MusicianDetail(LoginRequiredMixin, DetailView):
    model = Musician

class MusicianUpdate(LoginRequiredMixin, UpdateView):
    model = Musician
    fields = ['name', 'instrument']

class MusicianDelete(LoginRequiredMixin, DeleteView):
    model = Musician
    success_url = '/musicians/'

@login_required
def assoc_musician(request, record_id, musician_id):
    Record.objects.get(id=record_id).musicians.add(musician_id)
    return redirect('records_detail', record_id=record_id)

@login_required
def unassoc_musician(request, record_id, musician_id):
    Record.objects.get(id=record_id).musicians.remove(musician_id)
    return redirect('records_detail', record_id=record_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Something went wrong! Please try again.'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)