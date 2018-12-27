from django import forms


from django.shortcuts import render
from .fetcher import extract_basic_info_from_url
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

class URLForm(forms.Form):
    url = forms.fields.URLField()


@staff_member_required
def return_basic_info(request):
    # if request.isAjax()
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = request.POST['url']
            basic_info = extract_basic_info_from_url(url)
            return JsonResponse(basic_info)
        else:
            return HttpResponseBadRequest('Bad request')
    else:
        return HttpResponseNotAllowed(['POST'])
