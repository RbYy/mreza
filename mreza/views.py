from django.http import HttpResponse
from django.shortcuts import render
from mreza.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def mreza(request):
    return render(request, 'mreza/mreza.html')



# Create your views here.
