# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def jose(request):
    return HttpResponse('GAAAAY')

def bobo(request):
    return render(request, 'bobo.html')
