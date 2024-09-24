from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def providerPage(request):
    return render(request,'app/provider_page.html')
