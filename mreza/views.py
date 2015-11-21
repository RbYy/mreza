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
    nova_aktivna.aktivna=True
    nova_aktivna.save()
    batimenti_na_mrezi = Batiment.objects.filter(mreza=nova_aktivna)
   
    data1=serializers.serialize('json', batimenti_na_mrezi)
    data1_odkodirano=json.loads(data1)
    i=0
    for bat in batimenti_na_mrezi:

        pozx=Koordinate.objects.filter(batiment=bat).order_by('-id')[0].x
        pozy=Koordinate.objects.filter(batiment=bat).order_by('-id')[0].y 
        data1_odkodirano[i]['fields']['pozx']=pozx
        data1_odkodirano[i]['fields']['pozy']=pozy
        i+=1
        print('dddoootttooo')
        
    #data = serializers.serialize('json', kor)
    print(data1_odkodirano)
    data=serializers.serialize('json', [nova_aktivna,])
    
    #print(data1)
    return HttpResponse(data)
    
@login_required
def ustvari_batiment(request):
    novi_batiment=Batiment.objects.create(visina_bat=int(request.GET['visina']),
                            sirina_bat=int(request.GET['sirina']),
                            vrsta=request.GET['vrsta'],
                            ime=request.GET['ime'],
                            mreza=Mreza.objects.get(aktivna=True))
    print('do to')
    Koordinate.objects.create(
                              x=int(request.GET['offx']),
                              y=int(request.GET['offy']),
                              batiment=novi_batiment)
    print(Batiment.objects.all())
    
    
    print('----------------')
    print(Koordinate.objects.all())
    print(novi_batiment.id)
    return HttpResponse(str(novi_batiment.id))

@login_required
def zbrisi_batiment(request):
    print('vsaj pride notr')
    batiment_za_zbrisat = Batiment.objects.get(id=int(request.GET['id']))
    print(batiment_za_zbrisat.ime)
    batiment_za_zbrisat.delete()
    print(Batiment.objects.all().count())
    return HttpResponse('batiment zbrisan')

def shrani_nove_koordinate_batimenta(request):
    batiment=Batiment.objects.get(id=request.GET['id'])
    kor=Koordinate.objects.create(x=request.GET['offx'], y=request.GET['offy'], batiment=batiment)
    return HttpResponse(kor.x)
    
@login_required
def odjava(*args, **kwargs):
    logout(args[0])
    return HttpResponseRedirect('/accounts/login/')

# Create your views here.
