from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from uuid import uuid4
import json
from . import settings
from glob import glob
import os
from .models import fileupload
from .forms import fileuploadForm

CHUNKUPLOADPATH = settings.CHUNKUPLOADPATH

def home(request):
    return render(request, 'home.html')

def ajaxtest1(request):
    return render(request, 'ajaxtest1.html')

def ajaxtest2(request):
    return render(request, 'ajaxtest2.html', {'form' : fileuploadForm, 'formid': uuid4()} )

def ajaxtest3(request):
    return render(request, 'ajaxtest3.html', {'form' : fileuploadForm, 'formid': uuid4()} )

def post_chunkfileupload(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        uploadid = request.POST['uploadid']
        uploadid = uploadid.split('_')[1]
        chunkstatus = request.POST['chunkstatus']
        if chunkstatus == 'start': #len(uploadid) != 36:
            uploadid = str(uuid4())
            request.POST._mutable = True
            request.POST['uploadid'] = '0_' + uploadid
            request.POST._mutable = False
        # get the form data
        form = fileuploadForm(request.POST, request.FILES)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save(commit='no')
            instance.filename = request.FILES['thefile'].name
            instance.save()
            # serialize in new friend object in json
            # send to client side.
            return JsonResponse({"uploadid": uploadid}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)
    # some error occured
    return JsonResponse({"error": ""}, status=400)

def post_chunkfileupload_complete(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        uploadid = request.POST['uploadid']
        chunkstatus0 = request.POST['chunkstatus']
        chunkstatus = chunkstatus0.split('_')[0]
        nchunks = int(chunkstatus0.split('_')[1])
        if chunkstatus == 'complete':
            # not a good way, better to fetch from db
            files = glob(CHUNKUPLOADPATH + '*'+uploadid+'.part')
            cmd = 'cat '
            cmd1 = 'rm ' 
            for i in range(nchunks):
                cmd = cmd + '{0}{1}_{2}.part '.format(CHUNKUPLOADPATH, i, uploadid)
                cmd1 = cmd1 + '{0}{1}_{2}.part '.format(CHUNKUPLOADPATH, i, uploadid)
            cmd = cmd + '> {0}{1}.full '.format(CHUNKUPLOADPATH, uploadid)
            print('run '  + cmd)
            if len(files) == nchunks:
                status = os.system(cmd)
                if status != 0 :
                    print('chunkcomplete - cat failed', status, nchunks, len(files)) 
                    return JsonResponse({"error": 'cat failed'}, status=410)
                else:
                    status1 = os.system(cmd1) # just laxy to do it right way
                    #DO MD5 check
                    #TOD Add to form model table
                    #TOD  delete chunks from table
                    return JsonResponse({"uploadid": 'chunk upload complete'}, status=200)
            else:
                return JsonResponse({"error": 'upload failed - misssing file'}, status=410)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)
    # some error occured
    return JsonResponse({"error": ""}, status=400)

def post_fileupload(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        uploadid = uuid4()
        request.POST._mutable = True
        request.POST['uploadid'] = uploadid
        request.POST._mutable = False
        # get the form data
        form = fileuploadForm(request.POST, request.FILES)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save(commit='no')
            instance.filename = request.FILES['thefile'].name
            instance.save()
            # send to client side.
            return JsonResponse({"uploadid": uploadid}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)
    # some error occured
    return JsonResponse({"error": ""}, status=400)

def post_talk(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        #print(request.POST.get('data') )
        #print( json.loads( request.POST.get('data') ) )
        data = json.loads(request.POST.get('data'))
        #print( data['i'] )
        #print(data)
        # save the data and after fetch the object in instance
        # serialize in new friend object in json
        ndata = {'i':data['i'] + 1, 'msg':'added'}
        #ser_data = serializers.serialize('json', ndata)
        #print(ser_data)
        # send to client side.
        return JsonResponse({"data": ndata}, status=200)

    # some error occured
    return JsonResponse({"error": ""}, status=400)
