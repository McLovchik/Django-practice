from _csv import reader
from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render
from .models import Item
from .forms import UploadPriceForm


def items_list(request):
    items = Item.objects.all()
    return render(request, 'goods/items_list.html', {'items_list': items})


def update_prices(request):
    if request.method == 'POST':
        upload_file_form = UploadPriceForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            price_file = upload_file_form.cleaned_data['file'].read()
            price_str = price_file.decode('utf-8').split('\n')
            csv_reader = reader(price_str, delimiter=",", quotechar='"')
            for row in csv_reader:
                row_str = row[0].split(';')
                code = row_str[0]
                price = Decimal(row_str[1])
                Item.objects.filter(code=code).update(price=price)
            return HttpResponse(content='Цены были успешно обновлены', status=200)
    else:
        upload_file_form = UploadPriceForm()

    context = {
        'form': upload_file_form
    }
    return render(request, 'goods/upload_price_file.html', context=context)
