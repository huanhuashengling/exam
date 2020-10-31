from django.shortcuts import render
from django.contrib.auth.models import User
from account.models import Profile
import json
from utils.response import json_response

def normal_user_list(request):
    
    uid = request.session.get('uid', '')

    userData = []
    try:
        users = User.objects.all()

        for user in users:
            profile = Profile.objects.filter().get(name=user.username)
            user = User.objects.get(username=profile.name)  # 获取用户
            if not user.is_superuser:
                userData.append({'username': profile.name, 
                  'uid': profile.uid,
                  'phone': profile.phone,
                  'displayname': profile.displayname, 
                  'email': profile.email,
                  'is_staff': user.is_staff,
                  'is_active': user.is_active,
                  })
    except Profile.DoesNotExist:
        users = None
        return redirect(reverse("web_login"))
        # return render(request, 'web/login.html', {
        #     'login_info': settings.WXWEB_LOGIN_PARAMS or {},
        #     'has_login': False
        # })
    return render(request, 'web/user_list.html', {
        'userData': userData,
    })

def normal_user_list_data(request):
    
    uid = request.session.get('uid', '')

    userData = []
    try:
        users = User.objects.all().order_by("-date_joined")

        for user in users:
            profile = Profile.objects.filter().get(name=user.username)
            user = User.objects.get(username=profile.name)  # 获取用户
            tUserSrc = profile.get_user_src_display()

            if not user.is_superuser:
                userData.append({'username': profile.name, 
                  'uid': profile.uid,
                  'phone': profile.phone,
                  'displayname': profile.displayname, 
                  'classname': profile.classname, 
                  'email': profile.email,
                  'trainee_type': profile.get_trainee_type_display(),
                  'trainee_code': profile.trainee_code,
                  'user_src': tUserSrc,
                  'is_staff': user.is_staff,
                  'is_active': user.is_active,
                  })
    except Profile.DoesNotExist:
        users = None
        return redirect(reverse("web_login"))
        # return render(request, 'web/login.html', {
        #     'login_info': settings.WXWEB_LOGIN_PARAMS or {},
        #     'has_login': False
        # })
    return json_response(200, 'OK', {
        'userData': userData,
    })

def active_normal_user(request):
    activeUserId = request.POST.get('activeUserId', '')
    activeUsername = request.POST.get('activeUsername', '')
    try:
        user = User.objects.get(username=activeUsername)  # 获取用户
        user.is_active = True
        user.is_staff = True
        user.save()
    except User.DoesNotExist:
        user = None
    return json_response(200, 'OK', {
        'username': activeUsername,
    })


def deactive_normal_user(request):
    activeUserId = request.POST.get('activeUserId', '')  
    activeUsername = request.POST.get('activeUsername', '')
    try:
        user = User.objects.get(username=activeUsername)  # 获取用户
        user.is_active = False
        user.is_staff = False
        user.save()
    except User.DoesNotExist:
        user = None
    return json_response(200, 'OK', {
        'username': activeUsername,
    })
