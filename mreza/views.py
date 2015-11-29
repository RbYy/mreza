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
from lib2to3.pgen2.token import STAREQUAL


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
        grid = Mreza.objects.get(
                        uporabnik=request.user,
                        aktivna=True)
    except:
        grid=Mreza.objects.create(
                        ime='prva mreza',
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
    print('aaaa')
    for bat in batimenti_na_mrezi:
        print('poli')
        try:
            akt=Koordinate.objects.get(
                            batiment__mreza=aktivna_mreza,
                            aktivna=True)
            
            pozx=Koordinate.objects.filter(
                            batiment=bat,
                            pk__lte=akt.pk
                            ).order_by('-pk')[0].x
                            
            pozy=Koordinate.objects.filter(
                            batiment=bat,
                            pk__lte=akt.pk
                            ).order_by('-pk')[0].y
                            
            print('ddddddd')
        except:
            print('ss')    
        batimenti_json_odkodirano[i]['fields']['pozx']=pozx
        batimenti_json_odkodirano[i]['fields']['pozy']=pozy
        i+=1
    mreza_z_batimenti=mreza_json_odkodirano+batimenti_json_odkodirano
    mreza_z_batimenti_json=json.dumps(mreza_z_batimenti, cls=DjangoJSONEncoder)
    return HttpResponse(mreza_z_batimenti_json)
    
@login_required
def ustvari_batiment(request):
    aktivna_mreza=Mreza.objects.get(
                            uporabnik=request.user, 
                            aktivna=True)
    print('qqq')
    
    novi_batiment=Batiment.objects.create(
                            visina_bat=int(request.GET['visina']),
                            sirina_bat=int(request.GET['sirina']),
                            vrsta=request.GET['vrsta'],
                            ime=request.GET['ime'],
                            mreza=aktivna_mreza)
    print('www')
    try: #če je sploh že kakšen batiment na mreži
        #poisci kje je kazalec
        stare_koordinate=Koordinate.objects.get(
                            batiment__mreza=aktivna_mreza,
                            aktivna=True)
        
        #zbrisi vse poteze od kazalca naprej (onemogoci "redo")
        poteze_za_zbrisat = Koordinate.objects.filter(
                            batiment__mreza=aktivna_mreza,
                            pk__gt=stare_koordinate.pk)
        poteze_za_zbrisat.delete()        
        stare_koordinate.aktivna=False
        stare_koordinate.save()
        print('no exception')
    except:
        print('ni nobenega batimenta, da bi mu dal koordinate na False')
    print('eee')
    Koordinate.objects.create(
                            x=int(request.GET['offx']),
                            y=int(request.GET['offy']),
                            aktivna=True,
                            batiment=novi_batiment)
    print('rrr')
    return HttpResponse(str(novi_batiment.pk))

@login_required
def zbrisi_batiment(request):
    batiment_za_zbrisat = Batiment.objects.get(pk=int(request.GET['id']))
    batiment_za_zbrisat.delete()
    return HttpResponse('batiment zbrisan')

def shrani_nove_koordinate_batimenta(request):
    tbatiment=Batiment.objects.get(pk=request.GET['id'])
    
    #poisci kje je kazalec
    stare_koordinate = Koordinate.objects.get(aktivna=True, batiment__mreza__aktivna=True)
    print(stare_koordinate.aktivna)
    
    #zbrisi vse poteze od kazalca naprej (onemogoci "redo")
    poteze_za_zbrisat = Koordinate.objects.filter(
                                            batiment__mreza__aktivna=True,
                                            pk__gt=stare_koordinate.pk)
    poteze_za_zbrisat.delete()
    stare_koordinate.aktivna = False
    stare_koordinate.save()
    nove_koordinate=Koordinate.objects.create(
                                            x=int(request.GET['offx']), 
                                            y=int(request.GET['offy']),
                                            aktivna=True, 
                                            batiment=tbatiment)
    return HttpResponse(nove_koordinate.x)

@login_required
def nazaj(request):
    aktivna_mreza=Mreza.objects.get(uporabnik=request.user, aktivna=True)
    
    #vse koordinate na tej mrezi
    zgodovina_mreze=Koordinate.objects.filter(batiment__mreza = aktivna_mreza)
    
    #kazalec - aktualne koordinate
    trenutna_poteza = zgodovina_mreze.get(aktivna=True)
    print('eeeeeee')
    #batiment na potezi kjer je kazalec
    bat=trenutna_poteza.batiment
    
    try:
        #najdi predhodne koordinate tega batimenta
        #na [0] so trenutne koordinate batimenta, na [1] so koordinate ene poteze prej
        povrni=zgodovina_mreze.filter(
                                pk__lte=trenutna_poteza.pk,
                                batiment=bat
                                ).order_by('-pk')[1]         
        

        print('eee')

        response=serializers.serialize('json', [povrni,])
    except:
        print('exception')
        response=serializers.serialize('json', [trenutna_poteza,])
        print(response)
        response=json.loads(response)
        print('111')
        response.append('x')
        print('222')
        response=json.dumps(response, cls=DjangoJSONEncoder)
        print(response)
        
    try:    
        #najdi koordinate ene poteze nazaj absolutna, kamor naj se premakne kazalec
        poteza_nazaj=zgodovina_mreze.filter(
                            pk__lt=trenutna_poteza.pk
                            ).order_by('-pk')[0]
    except:
        return HttpResponse('["x", "y", "z"]')                               
    #premakni kazalec eno potezo nazaj
    trenutna_poteza.aktivna=False
    poteza_nazaj.aktivna=True
    trenutna_poteza.save()
    poteza_nazaj.save()    
    print(response)
    return HttpResponse(response)

@login_required
def naprej(request):
    aktivna_mreza=Mreza.objects.get(uporabnik=request.user, aktivna=True)
    zgodovina_mreze=Koordinate.objects.filter(batiment__mreza = aktivna_mreza)
    trenutna_poteza = zgodovina_mreze.get(aktivna=True)
    poteza_naprej=zgodovina_mreze.filter(
                                        pk__gt=trenutna_poteza.pk
                                        ).order_by('pk')[0]
    trenutna_poteza.aktivna=False
    poteza_naprej.aktivna=True
    trenutna_poteza.save()
    poteza_naprej.save()
    response=serializers.serialize('json', [poteza_naprej,])
    print(response)
    return HttpResponse(response)    

@login_required
def odjava(*args, **kwargs):
    logout(args[0])
    return HttpResponseRedirect('/accounts/login/')


