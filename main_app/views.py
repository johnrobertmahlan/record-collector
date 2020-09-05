from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Record, Listening, Musician, Photo
from .forms import ListeningForm
import uuid
import boto3
from botocore.exceptions import ClientError

# Create your views here.

S3_BASE_URL = "https://jrm-record-collector.s3.amazonaws.com/"
BUCKET = "jrm-record-collector"

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

class RecordList(ListView):
    model = Record

# def records_index(request):
#     records = Record.objects.all()
#     return render(request, 'records/index.html', {'records': records})

def records_detail(request, record_id):
    record = Record.objects.get(id=record_id)
    musicians_not_on_record = Musician.objects.exclude(id__in=record.musicians.all().values_list('id'))
    listening_form = ListeningForm()
    return render(request, 'records/detail.html', {'record': record, 'listening_form': listening_form, 'musicians': musicians_not_on_record})

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

class MusicianIndex(ListView):
    model = Musician

class MusicianCreate(CreateView):
    model = Musician
    fields = '__all__'

class MusicianDetail(DetailView):
    model = Musician

class MusicianUpdate(UpdateView):
    model = Musician
    fields = ['name', 'instrument']

class MusicianDelete(DeleteView):
    model = Musician
    success_url = '/musicians/'

def assoc_musician(request, record_id, musician_id):
    Record.objects.get(id=record_id).musicians.add(musician_id)
    return redirect('records_detail', record_id=record_id)

def unassoc_musician(request, record_id, musician_id):
    Record.objects.get(id=record_id).musicians.remove(musician_id)
    return redirect('records_detail', record_id=record_id)