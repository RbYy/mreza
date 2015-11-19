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
            aktivna_mreza=Mreza.objects.get(uporabnik=request.user, aktivna=True)
            print('najdena!!!!')
            aktivna_mreza.aktivna=False
            aktivna_mreza.save()
            print('do to je uredi')
            ustvarjena_mreza = Mreza.objects.create(
                             ime=request.GET['ime_mreze'],
                             datum=timezone.now(),
                             sirina=int(request.GET['sirina']),
                             visina=int(request.GET['visina']),
                             aktivna=True,
                             uporabnik=request.user,
                             )
            
        except:
            print('kje je ')
        
    except:
        print('napaka')
    print("pkpkpk", ustvarjena_mreza.pk)
    return HttpResponse(ustvarjena_mreza.pk)

@login_required
def povleci_mreze(request):
    print('dddd')
    try:
        vse_mreze = Mreza.objects.flter(uporabnik=request.user)
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
        grid = Mreza.objects.get(uporabnik=request.user, aktivna=True)
        print('obstaja')
    except:
        grid=Mreza.objects.create(ime='prva mreža',
                                  datum=timezone.now(),
                                  sirina=25,
                                  visina=25,
                                  aktivna=True,
                                  uporabnik=request.user)
        #grid = Mreza.objects.create(sirina=25, visina=25, uporabnik=request.user)
    vse_mreze=Mreza.objects.filter(uporabnik=request.user)    
    return render(request, 'mreza/mreza.html', {'default_mreza':grid,
                                                'vse_mreze':vse_mreze})

@login_required
def shrani_nove_dimenzije_mreze(request):
    mreza_za_updatat=Mreza.objects.get(uporabnik=request.user, aktivna=True)
    mreza_za_updatat.sirina=request.GET['sirina']
    mreza_za_updatat.visina=request.GET['visina']
    mreza_za_updatat.save()
    return HttpResponse('dd')

@login_required
def aktiviraj_drugo_mrezo(request):
    stara_aktivna=Mreza.objects.get(uporabnik=request.user, aktivna=True)
    
    stara_aktivna.aktivna=False
    stara_aktivna.save()
    nova_aktivna=Mreza.objects.get(pk=int(request.GET['pk']))
    print('debug', nova_aktivna)
    nova_aktivna.aktivna=True
    nova_aktivna.save()
    print('debug2')
    data=serializers.serialize('json', [nova_aktivna,])
    print('debug3', data)
    return HttpResponse(data)
    
@login_required
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
