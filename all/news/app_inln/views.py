from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.formats import date_format
import datetime


def inln_page_view(request):
    time_message = _('Today is %(date)s %(time)s') % {
        'date': date_format(datetime.datetime.now().date(), format='SHORT_DATE_FORMAT', use_l10n=True),
        'time': datetime.datetime.now().time()
    }
    return render(request, 'inln/inln.html', context={
        'time_message': time_message
    })
