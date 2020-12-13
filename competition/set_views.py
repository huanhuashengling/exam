# -*- coding: utf-8 -*-
import datetime
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from competition.models import BankInfo, CompetitionKindInfo
from business.models import BusinessAccountInfo, AppConfigInfo, BusinessAppInfo
from account.models import Profile

from utils.response import json_response
from utils.redis.rpageconfig import set_pageconfig
from utils.errors import SetError, BizError, ProfileError
from utils.decorators import check_login, logerr


def banks(request):
    banks = BankInfo.objects.order_by('-kind_num')
    bankData = []
    for bank in banks:
        bankData.append({'bank_name': bank.bank_name, 
                        'bank_id': bank.bank_id, 
                        'bank_type': bank.get_bank_type_display(), 
                        'kind_num': bank.kind_num, 
                        'total_question_num': bank.total_question_num,
                        'A1_choice_num': bank.A1_choice_num,
                        'A2_choice_num': bank.A2_choice_num,
                        'A3_choice_num': bank.A3_choice_num,
                        'B_choice_num': bank.B_choice_num,
                        'G_fillinblank_num': bank.G_fillinblank_num,
                        'partin_num': bank.partin_num,
                        })
    # return json_response(200, 'OK', {'banks': [{'bank_name': b[0], 'bank_id': b[1], 'kind_num': b[2], 'total_question_num': b[3] + b[4]} for b in banks]})
    return json_response(200, 'OK', {'banks': bankData})
    
    return json_response(*SetError.BankTypeError)

def get_a_bank(request):
    bank_id = request.GET.get('bank_id', '')

    bank = BankInfo.objects.filter(bank_id=bank_id).first()

    return json_response(200, 'OK', {'bank_name': bank.bank_name, 
                                    'bank_id': bank.bank_id,
                                    'kind_num': bank.kind_num, 
                                    'A1_choice_num': bank.A1_choice_num,
                                    'A2_choice_num': bank.A2_choice_num,
                                    'A3_choice_num': bank.A3_choice_num,
                                    'B_choice_num': bank.B_choice_num,
                                    'G_fillinblank_num': bank.G_fillinblank_num})

def bank_detail(request, bank_id):
    try:
        bank = BankInfo.objects.get(bank_id=bank_id)
    except BankInfo.DoesNotExist:
        return json_response(*SetError.BankInfoNotFound)

    return json_response(200, 'OK', {'bank_info': bank.data})

def bank_detail(request, bank_id):
    try:
        bank = BankInfo.objects.get(bank_id=bank_id)
    except BankInfo.DoesNotExist:
        return json_response(*SetError.BankInfoNotFound)

    return json_response(200, 'OK', {'bank_info': bank.data})
    
@logerr
@csrf_exempt
@check_login
@transaction.atomic
def set_bank(request):
    account_id = request.POST.get('account_id', '')
    uid = request.POST.get('uid', '')
    bank_id = request.POST.get('bank_id', '')
    kind_name = request.POST.get('kind_name', '')
    sponsor_name = int(request.POST.get('sponsor_name', 0))
    question_num = int(request.POST.get('question_num', 1))
    A1_choice_num = int(request.POST.get('A1_choice_num', 0))
    A2_choice_num = int(request.POST.get('A2_choice_num', 0))
    A3_choice_num = int(request.POST.get('A3_choice_num', 0))
    B_choice_num = int(request.POST.get('B_choice_num', 0))
    # G_fillinblank_num = int(request.POST.get('G_fillinblank_num', 0))
    # EG_fillinblank_num = int(request.POST.get('EG_fillinblank_num', 0))
    # S_fillinblank_num = int(request.POST.get('S_fillinblank_num', 0))
    # A_fillinblank_num = int(request.POST.get('A_fillinblank_num', 0))
    total_score = int(request.POST.get('total_score', 100))
    cop_startat = request.POST.get('cop_startat')
    cop_finishat = request.POST.get('cop_finishat')
    period = request.POST.get('period')
    rule_text = request.POST.get('rule_text', '')
    is_show_userinfo = request.POST.get('is_show_userinfo', 'false')
    form_data = request.POST.get('form_data', '')
    field_name_data = request.POST.get('field_name_data', '')
    option_data = request.POST.get('option_data', '')
    # is_open = request.POST.get('is_open', True)
    # print(request.POST.get('is_open'))
    # print(type(request.POST.get('is_open')))
    is_open = True if request.POST.get('is_open') == 'true' else False
    # print(is_open)
    # print(type(is_open))
    try:
        BusinessAccountInfo.objects.select_for_update().get(account_id=account_id)
    except BusinessAccountInfo.DoesNotExist:
        return json_response(*BizError.BizAccountNotFound)

    try:
        profile = Profile.objects.select_for_update().get(uid=uid)
    except Profile.DoesNotExist:
        return json_response(*ProfileError.ProfileNotFound)

    try:
        bank_info = BankInfo.objects.select_for_update().get(bank_id=bank_id)
    except BankInfo.DoesNotExist:
        return json_response(*SetError.BankInfoNotFound)

    app_info = BusinessAppInfo.objects.select_for_update().create(
        account_id=account_id,
        app_name=kind_name
    )

    app_config_values = {
        'app_name': kind_name,
        'rule_text': rule_text,
        'is_show_userinfo': True if is_show_userinfo == 'true' else False,
        'userinfo_fields': form_data.rstrip('#'),
        'userinfo_field_names': field_name_data.rstrip('#'),
        'option_fields': option_data.rstrip('#'),
    }

    app_config_info, app_config_created = AppConfigInfo.objects.select_for_update().get_or_create(
        app_id=app_info.app_id,
        defaults=app_config_values
    )

    if not app_config_created:
        for k, v in app_config_values.items():
            setattr(app_config_info, k, v)
        app_config_info.save()

    kind_values = {
        'kind_name': kind_name,
        'sponsor_name': sponsor_name,
        'kind_type': bank_info.bank_type,
        'total_score': total_score,
        'question_num': question_num,
        'A1_choice_num': A1_choice_num,
        'A2_choice_num': A2_choice_num,
        'A3_choice_num': A3_choice_num,
        'B_choice_num': B_choice_num,
        # 'G_fillinblank_num': G_fillinblank_num,
        # 'EG_fillinblank_num': EG_fillinblank_num,
        # 'S_fillinblank_num': S_fillinblank_num,
        # 'A_fillinblank_num': A_fillinblank_num,
        'cop_startat': cop_startat,
        'period_time': period or 0,
        'is_open': is_open,
        'cop_finishat': cop_finishat
    }

    # print(account_id)
    # print(app_info.app_id)
    # print(bank_id)
    # print(kind_values)
    kind_info, kind_created = CompetitionKindInfo.objects.select_for_update().get_or_create(
        account_id=account_id,
        app_id=app_info.app_id,
        bank_id=bank_id,
        defaults=kind_values
    )

    if not kind_created:
        for k, v in kind_values.items():
            setattr(kind_info, k, v)
        kind_info.save()

    set_pageconfig(app_config_info.data)

    return json_response(200, 'OK', {})

def game_list_data(request):
    kindData = []
    kinds = CompetitionKindInfo.objects.all()
    for kind in kinds:
        copStartat = kind.cop_startat.strftime("%Y/%m/%d")
        copFinishat = kind.cop_finishat.strftime("%Y/%m/%d")
        copFinishatValue = kind.cop_finishat.strftime("%Y-%m-%d")
        isOpen = "否"
        if kind.is_open:
            isOpen = "是"
        bank_info = BankInfo.objects.get(bank_id=kind.bank_id)
        kindData.append({'sponsor_name': kind.get_sponsor_name_display(),
                        'kind_name': kind.kind_name,
                        'kind_id': kind.kind_id,
                        'bank_name': bank_info.bank_name,
                        'kind_type': kind.get_kind_type_display(),
                        'total_score': kind.total_score,
                        'question_num': kind.question_num,
                        'A1_choice_num': kind.A1_choice_num,
                        'A2_choice_num': kind.A2_choice_num,
                        'A3_choice_num': kind.A3_choice_num,
                        'B_choice_num': kind.B_choice_num,
                        'cop_startat': copStartat,
                        'period': kind.period_time,
                        'cop_finishat': copFinishat,
                        'copFinishatValue': copFinishatValue,
                        'is_open': isOpen,
                        'is_open_value': kind.is_open,
                        'total_partin_num': kind.total_partin_num,
                        })

    return json_response(200, 'OK', {
        'data': kindData,
    })

def update_competition_kind_info(request):
    kind_id = request.POST.get('kind_id', '')
    uid = request.POST.get('uid', '')
    kind_name = request.POST.get('kind_name', '')
    kind_type = request.POST.get('kind_type', '')
    question_num = int(request.POST.get('question_num', 1))
    total_score = int(request.POST.get('total_score', 100))
    cop_finishat = request.POST.get('cop_finishat')
    period = request.POST.get('period') or 0
    is_open = True if request.POST.get('is_open') == 'true' else False

    kind_info = CompetitionKindInfo.objects.get(kind_id=kind_id)
    kind_info.kind_name = kind_name 
    kind_info.kind_type = kind_type 
    kind_info.total_score = total_score 
    kind_info.question_num = question_num 
    kind_info.cop_finishat = cop_finishat
    kind_info.period_time = period
    kind_info.is_open = is_open
    kind_info.save()

    return json_response(200, 'OK', {})
