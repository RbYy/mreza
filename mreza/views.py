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
    vidni_batimenti_na_mrezi = Batiment.objects.filter(
                            mreza=aktivna_mreza,
                            viden=True)
    batimenti_json=serializers.serialize('json', vidni_batimenti_na_mrezi)
    mreza_json=serializers.serialize('json', [aktivna_mreza,])
    batimenti_json_odkodirano=json.loads(batimenti_json)
    mreza_json_odkodirano=json.loads(mreza_json)
    i=0
    print('hhh')
    for bat in vidni_batimenti_na_mrezi:
        try:
            if Koordinate.objects.filter(batiment__mreza=aktivna_mreza, aktivna=True).count() == 0:
                #print('pogoj'+str(Koordinate.objects.filter(batiment__mreza=aktivna_mreza, aktivna=True).count()))
                a=Koordinate.objects.filter(
                           batiment__mreza=aktivna_mreza
                           ).order_by('-pk')[0]
                a.aktivna=True
                a.save()
            if Koordinate.objects.filter(batiment__mreza=aktivna_mreza, aktivna=True).count() > 1:
                #print('pogoj'+str(Koordinate.objects.filter(batiment__mreza=aktivna_mreza, aktivna=True).count()))
                a=Koordinate.objects.filter(
                           batiment__mreza=aktivna_mreza,
                           aktivna=True
                           ).order_by('pk')[0]
                a.aktivna=False
                a.save()            
            #print('pogoj'+str(Koordinate.objects.filter(batiment__mreza=aktivna_mreza, aktivna=True).count()))
            
            akt=Koordinate.objects.get(
                            batiment__mreza=aktivna_mreza,
                            aktivna=True)
            #print(akt)
            print('rrr')
            pozx=Koordinate.objects.filter(
                            batiment=bat,
                            pk__lte=akt.pk
                            ).order_by('-pk')[0].x
            print('www')                
            pozy=Koordinate.objects.filter(
                            batiment=bat,
                            pk__lte=akt.pk
                            ).order_by('-pk')[0].y

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
    
    
    novi_batiment=Batiment.objects.create(
                            visina_bat=int(request.GET['visina']),
                            sirina_bat=int(request.GET['sirina']),
                            vrsta=request.GET['vrsta'],
                            ime=request.GET['ime'],
                            mreza=aktivna_mreza,
                            viden=True)
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
    bat_bri =[]
    #iz baze odstrani batimente za brisat - onemogoči redo
    #briši tiste batimente, ki so bili ustvarjeni po trenutku na katerega kaze kazalec
    nevidni_batimenti=Batiment.objects.filter(viden=False, mreza__aktivna=True)
    for bat in nevidni_batimenti:
        prve_koordinate=bat.koordinate_set.all().order_by('pk')[0]
        #print(stare_koordinate.pk, prve_koordinate.pk)
        
        if stare_koordinate.pk < prve_koordinate.pk:
            print('0000')
            bat_bri.append(bat.pk) 
            bat.delete()
            print('polo')
        if bat.koordinate_set.filter(brisanje=True):
            
            koo_bri = bat.koordinate_set.filter(brisanje=True
                                                ).order_by('-pk')[0]
            if stare_koordinate.pk < koo_bri.pk:
                #print('stare: ',stare_koordinate.pk, '   koordinate ob brisanju: ',koo_bri.pk,'  brisanjeeeeeeeeeee')
                bat_bri.append(bat.pk)
                bat.delete() 
    print('ggg')    
    response=[{"brisi":bat_bri}, novi_batiment.pk]
    response=json.dumps(response, cls=DjangoJSONEncoder)
    
    
    print(response)
    return HttpResponse(response)

@login_required
def zbrisi_batiment(request):
    batiment_za_zbrisat = Batiment.objects.get(pk=int(request.GET['id']))
    batiment_za_zbrisat.viden=False
    batiment_za_zbrisat.save()
    kazalec=Koordinate.objects.get(batiment__mreza__aktivna=True, aktivna=True)
    kazalec.aktivna=False
    kazalec.save()
    #print(Koordinate.objects.filter(batiment__mreza__aktivna=True))
    koordinate_batimenta_za_brisat=Koordinate.objects.filter(
                                  batiment=batiment_za_zbrisat
                                  ).order_by('-pk')[0]
                                  
    print('brisi batiment  ', batiment_za_zbrisat.pk)                                  

    koordinate_batimenta_za_brisat.pk=None
    koordinate_batimenta_za_brisat.save()
    print('ddd',koordinate_batimenta_za_brisat.brisanje)
    koordinate_batimenta_za_brisat.save()
    for x in Koordinate.objects.filter(batiment=batiment_za_zbrisat).order_by('pk'):
        print('888')
        x.brisanje=False
        x.save()
        print('koordinate batimenta: pk: ',x.pk, '  --  brisanje: ',x.brisanje)
    zadnje_koordinate_ob_brisanju = Koordinate.objects.filter(
                                batiment=batiment_za_zbrisat
                                ).order_by('-pk')[0]
    zadnje_koordinate_ob_brisanju.brisanje=True
    zadnje_koordinate_ob_brisanju.aktivna=True
    zadnje_koordinate_ob_brisanju.save()
    #print('koordinate ob brisanju: ',zadnje_koordinate_ob_brisanju.brisanje)
    #print('ddd',koordinate_batimenta_za_brisat.brisanje)
    print(batiment_za_zbrisat)
    return HttpResponse(batiment_za_zbrisat.pk)

def shrani_nove_koordinate_batimenta(request):
    aktivna_mreza=Mreza.objects.get(aktivna=True, uporabnik=request.user)
    print(request.GET)
    for bat in Batiment.objects.filter(mreza=aktivna_mreza):
        print(bat)
    tbatiment=Batiment.objects.get(pk=str(request.GET['id']))
    #print('premakni batiment  ',tbatiment.pk)
    #poisci kje je kazalec
    stare_koordinate = Koordinate.objects.get(aktivna=True, batiment__mreza__aktivna=True)
    #print(stare_koordinate)
    bat_bri =[]
    #iz baze odstrani batimente za brisat - onemogoči redo
    #briši tiste batimente, ki so bili ustvarjeni po trenutku na katerega kaze kazalec
    nevidni_batimenti=Batiment.objects.filter(viden=False, mreza__aktivna=True)
    print(nevidni_batimenti)
    for bat in nevidni_batimenti:
        prve_koordinate=bat.koordinate_set.all().order_by('pk')[0]
        print(stare_koordinate.pk, prve_koordinate.pk)
        
        if stare_koordinate.pk < prve_koordinate.pk:
            print('0000')
            bat_bri.append(bat.pk) 
            bat.delete()
            print('polo')
        if bat.koordinate_set.filter(brisanje=True).count()>0:
            print('333, ',bat.koordinate_set.filter(brisanje=True).count())
            print('ooooooo',bat.koordinate_set.filter(brisanje=True)[0].x) #, bat.koordinate_set.filter(brisanje=True)[1].x)
            koo_bri = bat.koordinate_set.filter(brisanje=True
                                                ).order_by('-pk')[0]###
            print('lolololo')
            if stare_koordinate.pk < koo_bri.pk:
                print('09999')
                print('stare: ',stare_koordinate.pk, '   koordinate ob brisanju: ',koo_bri.pk,'  brisanjeeeeeeeeeee')
                bat_bri.append(bat.pk)
                bat.delete() 
    print('ggg')
       
    #zbrisi vse poteze od kazalca naprej (onemogoci "redo")
    poteze_za_zbrisat = Koordinate.objects.filter(
                                batiment__mreza__aktivna=True,
                                pk__gt=stare_koordinate.pk)
    poteze_za_zbrisat.delete()
    stare_koordinate.aktivna = False
    stare_koordinate.save()
    Koordinate.objects.create(
                                x=int(request.GET['offx']), 
                                y=int(request.GET['offy']),
                                aktivna=True, 
                                batiment=tbatiment)
    bat_bri=json.dumps(bat_bri, cls=DjangoJSONEncoder)
    return HttpResponse(bat_bri)

@login_required
def nazaj(request):
    aktivna_mreza=Mreza.objects.get(uporabnik=request.user, aktivna=True)
    #vse koordinate na tej mrezi
    zgodovina_mreze=Koordinate.objects.filter(batiment__mreza = aktivna_mreza)
    #kazalec - aktualne koordinate
    trenutna_poteza = zgodovina_mreze.get(aktivna=True)
    #batiment na potezi kjer je kazalec
    bat=trenutna_poteza.batiment
    #print('poteza z batimentom: ',bat.pk)
    try:
        #najdi predhodne koordinate tega batimenta
        #na [0] so trenutne koordinate batimenta, na [1] so koordinate ene poteze prej
        povrni=zgodovina_mreze.filter(
                                pk__lte=trenutna_poteza.pk,
                                batiment=bat
                                ).order_by('-pk')[1]
        print(povrni)       
        if bat.viden == False:
            #print('pokazi zbrisan batiment', bat)
            bat.viden = True
            bat.save()
            response=serializers.serialize('json', [povrni,])
            response=json.loads(response)
            response.append('x')
            response.append('x')
            response=json.dumps(response, cls=DjangoJSONEncoder)
            print(response)
            print(povrni)
        else:
            #1
            #print('premakni batiment na prejsnjo pozicijo', bat)
            response=serializers.serialize('json', [povrni,])
        print('eee')

        
    except:
        #2
        print('skrij batiment')
        bat.viden=False
        bat.save()
        print('exception')
        response=serializers.serialize('json', [bat,])
        #print(response)
        response=json.loads(response)
        response.append('x')
        response=json.dumps(response, cls=DjangoJSONEncoder)
        print(response)
        
    try:    
        #najdi koordinate ene poteze nazaj absolutna, kamor naj se premakne kazalec
        poteza_nazaj=zgodovina_mreze.filter(
                            pk__lt=trenutna_poteza.pk
                            ).order_by('-pk')[0]
                            
    except:
        return HttpResponse('['+str(bat.pk)+', "x", "y", "z"]')                               
    #premakni kazalec eno potezo nazaj
    trenutna_poteza.aktivna=False
    poteza_nazaj.aktivna=True
    trenutna_poteza.save()
    poteza_nazaj.save()    
    #print(response)
    return HttpResponse(response)

@login_required
def naprej(request):
    aktivna_mreza=Mreza.objects.get(uporabnik=request.user, aktivna=True)
    zgodovina_mreze=Koordinate.objects.filter(batiment__mreza = aktivna_mreza)
    trenutna_poteza = zgodovina_mreze.get(aktivna=True)
    poteza_naprej=zgodovina_mreze.filter(
                                        pk__gt=trenutna_poteza.pk
                                        ).order_by('pk')[0]
    if poteza_naprej.batiment.viden == False:
        poteza_naprej.batiment.viden = True
    batiment_viden=poteza_naprej.batiment.viden
    trenutna_poteza.aktivna=False
    poteza_naprej.aktivna=True
    trenutna_poteza.save()
    poteza_naprej.save()
    response=serializers.serialize('json', [poteza_naprej,])
    response=json.loads(response)
    response.append(str(batiment_viden).lower())
    response=json.dumps(response, cls=DjangoJSONEncoder)
    #print(response)
    return HttpResponse(response)    

@login_required
def odjava(*args, **kwargs):
    logout(args[0])
    return HttpResponseRedirect('/accounts/login/')


