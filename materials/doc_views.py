from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.db import transaction
from django.http.response import StreamingHttpResponse
from django.shortcuts import render

from django.http import HttpResponse
from account.models import Profile, UserInfo
from competition.models import BankInfo
from business.models import BusinessAccountInfo
from materials.models import Document, DownloadLog
from utils.decorators import check_login
from utils.errors import (FileNotFound, FileTypeError, ProfileNotFound,
                          TemplateNotFound, BizAccountNotFound)
from utils.small_utils import get_now_string, get_today_string
from utils.response import json_response
from django.http import FileResponse
from django.utils.encoding import escape_uri_path
from django.shortcuts import redirect
import os

@check_login
def index(request):
    """
    题库和比赛导航页
    :param request: 请求对象
    :return: 渲染视图和user_info用户信息数据
    """

    uid = request.GET.get('uid', '')

    try:
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        return render(request, 'err.html', ProfileNotFound)

    return render(request, 'materials/index.html', {'user_info': profile.data})

@check_login
def documents(request):
    documents = Document.objects.all()
    documentData = []
    for document in documents:
        downloadCount = DownloadLog.objects.filter(doc_id=document.id).count()
        documentData.append({'id': document.id, 
                        'doc_name': document.doc_name, 
                        'file_type': document.file_type, 
                        'upload_date': document.upload_date.strftime("%Y-%m-%d %H:%M"), 
                        'download_count': downloadCount,
                        })
    return json_response(200, 'OK', {'documents': documentData})

@check_login
def add(request):
    uid = request.GET.get('uid', '')
    return render(request, 'materials/add.html')

@check_login
def doc_upload(request):
    uid = request.session.get('uid', '')

    if request.method == "POST":    # 请求方法为POST时，进行处理
        obj_list = request.FILES.getlist('files')
        for myFile in obj_list:

            # myFile = request.FILES["input-doc"]    # 获取上传的文件，如果没有文件，则默认为None 

            if not myFile:
                return json_response(200, 'OK', {"input_doc": "no files for upload!"})

            open_path = os.path.join(settings.UPLOADS_DIR, myFile.name)

            if os.path.exists(open_path):
                return json_response(200, 'OK', {"input_doc": "doc has exist!"})

            destination = open(open_path,'wb+')    # 打开特定的文件进行二进制的写操作 
            for chunk in myFile.chunks():      # 分块写入文件 
                destination.write(chunk)  
            destination.close()

            filename = myFile.name.rsplit('.', 1)

            name = filename[0]
            ext = filename[1]

            document = Document.objects.select_for_update().create(
                doc_name=myFile.name,
                file_type=ext
            )
    return redirect('/materials?uid=' + uid)
    # return json_response(200, 'OK', {"input_doc": "upload over!"})

@check_login
def doc_delete(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理 
        docId = request.POST.get('docId', '') 
    if not docId:
        return json_response(200, 'OK', {"input_doc": "no docId!"})

    document = Document.objects.get(id=docId)

    if not document:
        return json_response(200, 'OK', {"input_doc": "no document in model!"})

    filename = os.path.join(settings.UPLOADS_DIR, document.doc_name)

    Document.objects.filter(id=docId).delete()
    DownloadLog.objects.filter(doc_id=docId).delete()

    if not os.path.exists(filename):
        return json_response(200, 'OK', {"input_doc": "no file in dir!"})
    else:
        os.remove(filename)
    
    return json_response(200, 'OK', {"input_doc": "delete over!"})

def download(request):
    uid = request.session.get('uid', '')

    docId = request.GET.get('docId', '')
    document = Document.objects.get(id=docId)
    doc_path = os.path.join(settings.UPLOADS_DIR, document.doc_name)

    file=open(doc_path,'rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']="attachment; filename*=utf-8''{}".format(escape_uri_path(document.doc_name))

    DownloadLog.objects.select_for_update().create(
        doc_id=docId,
        user_id=uid,
    )
    return response