from django.http import HttpResponse
from django.shortcuts import render
from mreza.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from datetime import datetime
import json
from django.core import serializers
from django.db.models import Max, Sum
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone


# Create your views here.

@login_required
def ustvari_mrezo(request):
    try:
        print(request.user, request.GET['ime_mreze'],timezone.now(),int(request.GET['sirina']),
                             int(request.GET['visina']),
                             request.user)
        try:
            aktivna_mreza=Mreza.objects.get(aktivna=True)
            print('najdena!!!!')
            aktivna_mreza.aktivna=False
            aktivna_mreza.save()
        except:
            print('kje je ')
        
        Mreza.objects.create(
                             ime=request.GET['ime_mreze'],
                             datum=timezone.now(),
                             sirina=int(request.GET['sirina']),
                             visina=int(request.GET['visina']),
                             aktivna=True,
                             uporabnik=request.user,
                             )
    except:
        print('napaka')
    return HttpResponse('d')
@login_required
def povleci_mreze(request):
    print('dddd')
    try:
        vse_mreze = Mreza.objects.all()
        print('do sem')
        data=serializers.serialize('json', vse_mreze)
        
        #data = json.dumps(vse_mreze, cls=DjangoJSONEncoder)
    except:
        data="ni shranjenih mrež"
    print(data)
    return HttpResponse(data)

@login_required
def mreza(request):
    try:
        grid = Mreza.objects.get(aktivna=True)
        print('obstaja')
    except:
        pass
        #grid = Mreza.objects.create(sirina=25, visina=25, uporabnik=request.user)
    return render(request, 'mreza/mreza.html', {'default_mreza':grid})

def shrani(request):
    offx=int(request.GET['offx'])
    offy=int(request.GET['offy'])
    visina=int(request.GET['visina'])
    sirina=int(request.GET['sirina'])
    barva=request.GET['barva']
    ime=request.GET['ime']
    vrsta=request.GET['vrsta']

    return HttpResponse("d")

@login_required
def odjava(*args, **kwargs):
    logout(args[0])
    return HttpResponseRedirect('/accounts/login/')

# Create your views here.
