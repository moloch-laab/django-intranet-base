from django.shortcuts import render
from .models import Document


def index(request):
    documents = Document.objects.all()
    return render(request, "cartolas_gremios/cartolas_gremios.html", {'documents':documents})
