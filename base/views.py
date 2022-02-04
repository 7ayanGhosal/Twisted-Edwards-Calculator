from django import forms
from django.shortcuts import render
from base import forms,t_edwards
from sympy import nextprime
import math

# Create your views here.
a = 0
d = 0
p = 0
new_p = 0
set = False

def home(request):
    global a,d,p,new_p,set
    new_p = 0
    prime = 0
    adp_form = forms.adp_form()

    if request.method == "POST":

        adp_form = forms.adp_form(request.POST)

        if adp_form.is_valid():
            
            a = adp_form.cleaned_data['a']
            d = adp_form.cleaned_data['d']
            p = adp_form.cleaned_data['p']
            set = True
            new_p = nextprime(p-1)
            prime = (new_p == p)
            return render(request, 'base/home.html', {'adp_form': adp_form, 'stage': 2, 'a': a, 'd': d, 'p': p, 'new_p': new_p, 'time': math.ceil(new_p*math.log2(new_p)/10000000), 'prime': prime})
    return render(request, 'base/home.html', {'adp_form': adp_form, 'stage': 1})

def calc(request):
    global a,d,p,new_p,set
    if not set:
        return render(request,'base/notset.html')
    else:
        points = t_edwards.generatePoints(a,d,new_p)
        opt_form = forms.opt_form()
        
        if request.method == "POST":

            opt_form = forms.opt_form(request.POST)
            
            if opt_form.is_valid():

                opt = opt_form.cleaned_data['opt']
                x1 = opt_form.cleaned_data['x1']
                y1 = opt_form.cleaned_data['y1']
                x2 = opt_form.cleaned_data['x2']
                y2 = opt_form.cleaned_data['y2']

                # print(x1,y1,x2,y2)

                x_res = 0
                y_res = 0

                if(opt == '2'):
                    (x_res,y_res) = t_edwards.addpoints(a,d,new_p,(x1,y1), (x2,y2))
                elif(opt == '3'):
                    (x_res,y_res) = t_edwards.substractpoints(a,d,new_p,(x1,y1), (x2,y2))
                elif(opt == '4'):
                    (x_res,y_res) = t_edwards.doublepoint(a,d,new_p,(x1,y1))
                elif(opt == '5'):
                    (x_res,y_res) = t_edwards.multiplypoint(a,d,new_p,(x1,y1), x2)

                return render(request,'base/calculate.html',{'opt_form': opt_form, 'a': a, 'd': d, 'p': new_p, 'xarray': points[0], 'yarray': points[1], 'Array': zip(points[0], points[1]), 'x_res': x_res, 'y_res': y_res, 'result': True})

        return render(request,'base/calculate.html',{'opt_form': opt_form, 'a': a, 'd': d, 'p': new_p, 'xarray': points[0], 'yarray': points[1], 'Array': zip(points[0], points[1])})