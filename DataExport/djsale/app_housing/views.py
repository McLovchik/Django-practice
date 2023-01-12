from django.views.generic import ListView, TemplateView, DetailView
from .models import HousingObject


class About(TemplateView):
    template_name = 'real_estate/about.html'


class Contacts(TemplateView):
    template_name = 'real_estate/contacts.html'


class HousingObjectListView(ListView):
    model = HousingObject
    template_name = 'real_estate/real_estate_list.html'
    context_object_name = 'real_estate_list'


class HousingObjectDetailView(DetailView):
    model = HousingObject
    template_name = 'real_estate/real_estate_detail.html'
