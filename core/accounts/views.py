# Create your views here.
from .tasks import sendEmail

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page

import time
import requests

def send_email(request):
    sendEmail() # Send email with 5 seconds delay.
    return HttpResponse("<h1> Done@!with 5 second delay. </h1>")


@cache_page(60)
def test_server(request):
    response = requests.get("https://35a6a47b-3ae6-452b-8737-df03f2ee211a.mock.pstmn.io/test/delay/5")
    return JsonResponse(response.json())