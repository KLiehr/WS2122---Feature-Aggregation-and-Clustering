from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Doc
from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import shutil
# Create your views here.

def home(request):
    return render(request, 'ProjectApp/home.html')


def importCSVXES(request):
    return render(request, 'ProjectApp/Import.html')


def attributes(request):
    return render(request, 'ProjectApp/Attributes.html')


def userguide(request):
    try:
        return FileResponse(open('Requirements_Specification- Feature Aggregation in Process Mining.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

def file_upload_view(request):
    if request.method == 'POST':
        shutil.rmtree("media\eventlog")
        my_file = request.FILES.get('file')
        Doc.objects.create(upload=my_file)
        return HttpResponse('')
    return JsonResponse({'post':'false'})

@csrf_exempt
def updateeventlog(request):
    if request.method == 'POST':
        AttributesToDerive = request.body
        AttributesToDerive = AttributesToDerive.decode('utf-8')
        print(type(AttributesToDerive))
        print(AttributesToDerive)
    return JsonResponse({'post':'false'})

