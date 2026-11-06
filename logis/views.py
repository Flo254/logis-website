from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def services(request):
    return render(request,'services.html')

def service_details(request):
    return render(request,'service_details.html')

def getaquote(request):
    return render(request,'getaquote.html')

def starterpage(request):
    return render(request,'starterpage.html')

def pricing(request):
    return render(request,'pricing.html')
