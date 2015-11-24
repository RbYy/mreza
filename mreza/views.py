from django.http import HttpResponse
from django.shortcuts import render
from mreza.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone


@login_required
def ustvari_mrezo(request):
    aktivna_mreza=Mreza.objects.get(uporabnik=request.user, aktivna=True)
    batimenti_na_aktivni_mrezi = Batiment.objects.filter(mreza=aktivna_mreza)
    nova_mreza=aktivna_mreza
    nova_mreza.pk=None
    nova_mreza.save()   
    nova_mreza.ime=request.GET['ime_mreze']
    nova_mreza.datum=timezone.now()
    nova_mreza.save()
    for batiment in batimenti_na_aktivni_mrezi:
        koordinate_za_kopirat=batiment.koordinate_set.all().order_by('pk')
        batiment.pk=None 
        batiment.save()
        batiment.mreza=nova_mreza
        batiment.save()
        for koordinata in koordinate_za_kopirat:
            koordinata.pk=None
            koordinata.save()
            koordinata.batiment=batiment
            koordinata.save()
    aktivna_mreza.aktivna=False
    aktivna_mreza.save()
    return HttpResponse(nova_mreza.pk)

@login_required
def povleci_mreze(request):
    try:
        vse_mreze = Mreza.objects.flter(uporabnik=request.user)
        data=serializers.serialize('json', vse_mreze)
    except:
        data="ni shranjenih mrež"
    return HttpResponse(data)



@login_required
def shrani_nove_dimenzije_mreze(request):
    mreza_za_updatat=Mreza.objects.get(uporabnik=request.user, aktivna=True)
    mreza_za_updatat.sirina=request.GET['sirina']
    mreza_za_updatat.visina=request.GET['visina']
    mreza_za_updatat.save()
    return HttpResponse('dd')

@login_required
def mreza(request):
    try:
        grid = Mreza.objects.get(uporabnik=request.user, aktivna=True)
    except:
        grid=Mreza.objects.create(ime='prva mreza',
                                  datum=timezone.now(),
                                  sirina=25,
                                  visina=25,
                                  aktivna=True,
                                  uporabnik=request.user)
    vse_mreze=Mreza.objects.filter(uporabnik=request.user)    
    return render(request, 'mreza/mreza.html', {'default_mreza':grid,
                                                'vse_mreze':vse_mreze})
    
@login_required
def aktiviraj_drugo_mrezo(request):
    stara_aktivna=Mreza.objects.get(uporabnik=request.user, aktivna=True)
    stara_aktivna.aktivna=False
    stara_aktivna.save()
    nova_aktivna=Mreza.objects.get(pk=int(request.GET['pk']))
    nova_aktivna.aktivna=True
    nova_aktivna.save()
    return poslji_komplet(request)
    
def poslji_komplet(request): #poslje mrezo izpolnjeno z batimenti
    aktivna_mreza=Mreza.objects.get(uporabnik=request.user, aktivna=True)
    batimenti_na_mrezi = Batiment.objects.filter(mreza=aktivna_mreza)
    batimenti_json=serializers.serialize('json', batimenti_na_mrezi)
    mreza_json=serializers.serialize('json', [aktivna_mreza,])
    batimenti_json_odkodirano=json.loads(batimenti_json)
    mreza_json_odkodirano=json.loads(mreza_json)
    i=0
    for bat in batimenti_na_mrezi:
        pozx=Koordinate.objects.filter(batiment=bat).order_by('-pk')[0].x
        pozy=Koordinate.objects.filter(batiment=bat).order_by('-pk')[0].y
        batimenti_json_odkodirano[i]['fields']['pozx']=pozx
        batimenti_json_odkodirano[i]['fields']['pozy']=pozy
        i+=1
    mreza_z_batimenti=mreza_json_odkodirano+batimenti_json_odkodirano
    mreza_z_batimenti_json=json.dumps(mreza_z_batimenti, cls=DjangoJSONEncoder)
    return HttpResponse(mreza_z_batimenti_json)
    
@login_required
def ustvari_batiment(request):
    novi_batiment=Batiment.objects.create(visina_bat=int(request.GET['visina']),
                            sirina_bat=int(request.GET['sirina']),
                            vrsta=request.GET['vrsta'],
                            ime=request.GET['ime'],
                            mreza=Mreza.objects.get(uporabnik=request.user, aktivna=True))
    Koordinate.objects.create(
                              x=int(request.GET['offx']),
                              y=int(request.GET['offy']),
                              batiment=novi_batiment)
    return HttpResponse(str(novi_batiment.pk))

@login_required
def zbrisi_batiment(request):
    batiment_za_zbrisat = Batiment.objects.get(pk=int(request.GET['id']))
    batiment_za_zbrisat.delete()
    return HttpResponse('batiment zbrisan')

def shrani_nove_koordinate_batimenta(request):
    tbatiment=Batiment.objects.get(pk=request.GET['id'])
    kor=Koordinate.objects.create(x=int(request.GET['offx']), y=int(request.GET['offy']), batiment=tbatiment)
    return HttpResponse(kor.x)
    
@login_required
def odjava(*args, **kwargs):
    logout(args[0])
    return HttpResponseRedirect('/accounts/login/')


