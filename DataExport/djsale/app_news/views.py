from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
from django.views import generic

from .models import NewsItem


def get_news_in_custom_format(request):
    format = request.GET['format']
    if format not in ['json']:
        return HttpResponseBadRequest()
    data = serializers.serialize(format, NewsItem.objects.all())
    return HttpResponse(data)


class NewsItemDetailView(generic.DetailView):
    model = NewsItem
    template_name = 'news/newsitem_detail.html'


class NewsListView(generic.ListView):
    model = NewsItem
    ordering = ['-published_at']
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
