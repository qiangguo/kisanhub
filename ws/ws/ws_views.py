from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.shortcuts import render, redirect
from data_collection import crawler, data_request
from data_modelling import regression
import numpy

def start(request):
    t = get_template('index.html')
    html = t.render({})
    return HttpResponse(html)


def region_profile(request):
    t = get_template('region_profile.html')
    html = t.render({})
    
    if request.method=='GET':
        return HttpResponse(html)
    if request.method=='POST':
        region_name = request.POST.get('region_name')
        resource_type = request.POST.get('resource_type')
        present_type = request.POST.get('present_type')
        url = request.POST.get('url')
        Inputs = (region_name, resource_type, present_type, url)
        status, rtn = data_request.save_region_profile(*Inputs)
        if status=='OK':
            return HttpResponse(html)
        else:
            err = get_template('error.html')
            err_html = err.render({'reason': rtn})
            return HttpResponse(err_html)

    
def crawl_data(request):
    resources = data_request.read_all_region_profile()
    resources = ['-'.join(V) for V in resources]
    if request.method=='GET':
        t = get_template('crawler.html')
        html = t.render({'resource_records':resources})
        return HttpResponse(html)

    if request.method=='POST':
        inputs = request.POST.get('url')
        region, url, resource_type, order = inputs.split('-')
        s, c = data_request.crawl_and_save_data(region, url, resource_type, order)
        if s=='OK':
            t = get_template('crawler.html')
            html = t.render({'resource_records':resources})
            return HttpResponse(html)
        else:
            err = get_template('error.html')
            err_html = err.render({'reason': c})
            return HttpResponse(err_html)


def max_min_regression(request):
    """ """
    RegModel = regression.Regression()
    status, content = RegModel.get_data()
    if status=='ERROR':
        err = get_template('error.html')
        err_html = err.render({'reason': content})
        return HttpResponse(err_html)
        
    A, B = content
    V = RegModel.standRegres(A, B)
    V = V.tolist()

    Scale = 50
    YShift = 200
    
    # produce a model y = bx + a
    b = V[0][0]
    a = V[1][0]

    startPointX = 0
    startPointY = int(a*startPointX+b)
    
    endPointX = 1200
    endPointY = int(a*endPointX+b)

    X = [int(V2*Scale) for [V1, V2] in A]
    Y = [int(V*Scale)+YShift for V in B]
    points = []
    for x,y in zip(X, Y):
        points.append((x, y))
    
    t = get_template('max_min_regression.html')
    html = t.render({
        'points': points,
        'startPointX': startPointX,
        'startPointY': startPointY,
        'endPointX': endPointX,
        'endPointY': endPointY
    })
    return HttpResponse(html)
