from django.http import HttpResponse

def greeting(request):
    return HttpResponse("Welcome to line server. Add line index at the end of URL and get the text.")