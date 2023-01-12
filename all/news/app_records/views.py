from django.shortcuts import render, redirect
from django.views import generic
from .models import Record, RecordImage
from .forms import RecordModelForm, RecordImageModelForm, UploadRecordForm
from django.contrib.auth.decorators import login_required
from _csv import reader
from django.http import HttpResponse
# from django.views.decorators.cache import cache_page
# from time import sleep


# @cache_page(30)  # 30 seconds
@login_required
def create_record(request):
    # sleep(4)
    user = request.user
    if request.method == 'POST':
        record_form = RecordModelForm(request.POST)
        image_form = RecordImageModelForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        if record_form.is_valid() and image_form.is_valid():
            record_instance = record_form.save(commit=False)
            record_instance.author = user
            record_instance.save()
            for image in images:
                image_instance = RecordImage(image=image, record=record_instance)
                image_instance.save()
            return redirect('/records')
    else:
        record_form = RecordModelForm()
        image_form = RecordImageModelForm()
    return render(request, 'records/create_record.html', {
        'record_form': record_form,
        'image_form': image_form
    })


class RecordsListView(generic.ListView):
    model = Record
    template_name = 'records/records_list.html'
    context_object_name = 'records_list'
    queryset = Record.objects.order_by('-created_at')


class RecordDetailView(generic.DetailView):
    model = Record
    template_name = 'records/record_detail.html'
    context_object_name = 'record'

    def get_context_data(self, **kwargs):
        context = super(RecordDetailView, self).get_context_data(**kwargs)
        context['images'] = RecordImage.objects.all().filter(record_id=self.kwargs['pk'])
        return context


@login_required
def create_record_csv(request):
    user = request.user
    if request.method == 'POST':
        upload_records_form = UploadRecordForm(request.POST, request.FILES)
        if upload_records_form.is_valid():
            records_file = upload_records_form.cleaned_data['file'].read()
            records_str = records_file.decode('utf-8').split('\n')
            csv_reader = reader(records_str, delimiter=",", quotechar='"')
            for row in csv_reader:
                row_str = row[0].split(';')
                text = row_str[0]
                date_create = row_str[1]
                record = Record(
                    author=user,
                    text=text
                )
                record.save()
                record.created_at = date_create
                record.save()
            return HttpResponse(content='Записи успешно добавлены', status=200)
    else:
        upload_records_form = UploadRecordForm()

    context = {
        'form': upload_records_form
    }
    return render(request, 'records/upload_records_form.html', context=context)
