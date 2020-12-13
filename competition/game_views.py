# -*- coding: utf-8 -*-
import os
import io
import datetime
import random

from django.http import FileResponse
from reportlab.pdfgen import canvas

from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from account.models import Profile, UserInfo
from competition.models import (BankInfo, ChoiceInfo, CompetitionKindInfo,
                                CompetitionQAInfo, FillInBlankInfo, QuestionGroupInfo)
from TimeConvert import TimeConvert as tc

from utils.check_utils import check_correct_num
from utils.decorators import check_copstatus, check_login
from utils.errors import BankInfoNotFound, CompetitionError, ProfileError
from utils.redis.rprofile import enter_userinfo
from utils.redis.rrank import add_to_rank
from utils.response import json_response


@check_login
@check_copstatus
@transaction.atomic
def get_questions(request):
    """
    获取题目信息接口
    :param request: 请求对象
    :return: 返回json数据: user_info: 用户信息;kind_info: 比赛信息;qa_id: 比赛答题记录;questions: 比赛随机后的题目;
    """
    kind_id = request.GET.get('kind_id', '')  # 获取kind_id
    uid = request.GET.get('uid', '')  # 获取uid
    #一次只有一条在测试的记录，提交之后的测试不会被删除
    CompetitionQAInfo.objects.filter(
        kind_id=kind_id,
        uid=uid,
        started=True,
        finished=False,
    ).delete()

    try:  # 获取比赛信息
        kind_info = CompetitionKindInfo.objects.select_for_update().get(kind_id=kind_id)
    except CompetitionKindInfo.DoesNotExist:  # 未获取到，返回错误码100001
        return json_response(*CompetitionError.CompetitionNotFound)
    try:  # 获取题库信息
        bank_info = BankInfo.objects.get(bank_id=kind_info.bank_id)
    except BankInfo.DoesNotExist:  # 未获取到，返回错误码100004
        return json_response(*CompetitionError.BankInfoNotFound)
    try:  # 获取用户信息
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:  # 未获取到，返回错误码200001
        return json_response(*ProfileError.ProfileNotFound)
    

    A3QuestionGroup = QuestionGroupInfo.objects.filter(bank_id=kind_info.bank_id).filter(question_group_type=1) # A3选择题
    BQuestionGroup = QuestionGroupInfo.objects.filter(bank_id=kind_info.bank_id).filter(question_group_type=2) # B选择题
    
    A3QuestionGroups = []
    for i in A3QuestionGroup.iterator():
        A3QuestionGroups.append(i.data)
    A3QuestionGroups = random.sample(A3QuestionGroups, kind_info.A3_choice_num)

    BQuestionGroups = []
    for i in BQuestionGroup.iterator():
        BQuestionGroups.append(i.data)
    BQuestionGroups = random.sample(BQuestionGroups, kind_info.B_choice_num)

    A3QuestionNum = 0
    A3qs = []
    for i in A3QuestionGroups:
        A3chioces = ChoiceInfo.objects.filter(question_group_id=i["pk"])
        for j in A3chioces.iterator():
            A3QuestionNum += 1
            A3data = j.data
            A3data.update({"group_question_txt":i["group_question_txt"]})
            A3data.update({"group_question_count":i["group_question_count"]})
            A3qs.append(A3data)

    BQuestionNum = 0
    Bqs = []
    for i in BQuestionGroups:
        Bchioces = ChoiceInfo.objects.filter(question_group_id=i["pk"])
        for j in Bchioces.iterator():
            BQuestionNum += 1
            Bdata = j.data
            Bdata.update({"group_question_count":i["group_question_count"]})
            Bqs.append(Bdata)

    actualQuestionNum = kind_info.A1_choice_num + kind_info.A2_choice_num + A3QuestionNum + BQuestionNum

    newA1ChoiceNum = kind_info.A1_choice_num
    newA2ChoiceNum = kind_info.A2_choice_num
    if actualQuestionNum < kind_info.question_num:
        diff = kind_info.question_num - actualQuestionNum
        newA1ChoiceNum = newA1ChoiceNum + diff//2
        newA2ChoiceNum = newA2ChoiceNum + diff//2
        newA1ChoiceNum = newA1ChoiceNum + diff%2
        
    # qf = FillInBlankInfo.objects.filter(bank_id=kind_info.bank_id)  # 填空题


    A1qc = ChoiceInfo.objects.filter(bank_id=kind_info.bank_id).filter(ctype=1) # A1选择题
    A2qc = ChoiceInfo.objects.filter(bank_id=kind_info.bank_id).filter(ctype=2) # A2选择题
    
    A1questions = []
    for i in A1qc.iterator():
        A1questions.append(i.data)
    A1qs = random.sample(A1questions, newA1ChoiceNum)

    A2questions = []
    for i in A2qc.iterator():
        A2questions.append(i.data)
    A2qs = random.sample(A2questions, newA2ChoiceNum)

    qs = A1qs + A2qs + A3qs + Bqs  # 将两种题型放到同一个列表中
    # for i in qc.iterator():
    #     questions.append(i.data)

    # for i in qf.iterator():
    #     questions.append(i.data)
    question_num = kind_info.question_num  # 出题数
    q_count = bank_info.total_question_num  # 总题数
    if q_count < question_num:  # 出题数大于总题数，返回错误码100005
        return json_response(CompetitionError.QuestionNotSufficient)
    # qs = random.sample(questions, question_num)  # 随机分配题目
    qa_info = CompetitionQAInfo.objects.select_for_update().create(  # 创建答题log数据
        kind_id=kind_id,
        uid=uid,
        qsrecord=[q['question'] for q in qs],
        asrecord=[q['answer'] for q in qs],
        total_num=question_num,
        started_stamp=tc.utc_timestamp(ms=True, milli=True),  # 设置开始时间戳
        started=True
    )
    for i in qs:  # 剔除答案信息
        tAnswers = i['answer'].split("|");
        if len(tAnswers) > 1:
            i['multiChoice'] = True
        else:
            i['multiChoice'] = False
        # i.pop('answer')
    return json_response(200, 'OK', {  # 返回JSON数据，包括题目信息，答题log信息等
        'kind_info': kind_info.data,
        'user_info': profile.data,
        'qa_id': qa_info.qa_id,
        'questions': qs
    })

@csrf_exempt
@check_login
@check_copstatus
@transaction.atomic
def submit_answer(request):
    """
    提交答案接口
    :param request: 请求对象
    :return: 返回json数据: user_info: 用户信息; qa_id: 比赛答题记录标识; kind_id: 比赛唯一标识
    """
    stop_stamp = tc.utc_timestamp(ms=True, milli=True)  # 结束时间戳
    qa_id = request.POST.get('qa_id', '')  # 获取qa_id
    uid = request.POST.get('uid', '')  # 获取uid
    kind_id = request.POST.get('kind_id', '')  # 获取kind_id
    answer = request.POST.get('answer', '')  # 获取answer

    try:  # 获取比赛信息
        kind_info = CompetitionKindInfo.objects.get(kind_id=kind_id)
    except CompetitionKindInfo.DoesNotExist:  # 未获取到，返回错误码100001
        return json_response(*CompetitionError.CompetitionNotFound)
    try:  # 获取题库信息
        bank_info = BankInfo.objects.get(bank_id=kind_info.bank_id)
    except BankInfo.DoesNotExist:  # 未获取到返回错误码100004
        return json_response(*CompetitionError.BankInfoNotFound)
    try:  # 获取用户信息
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:  # 未获取到，返回错误码200001
        return json_response(*ProfileError.ProfileNotFound)
    try:  # 获取答题log信息
        qa_info = CompetitionQAInfo.objects.select_for_update().get(qa_id=qa_id)
    except CompetitionQAInfo.DoesNotExist:  # 未获取到，返回错误码100006
        return json_response(*CompetitionError.QuestionNotFound)

    answer = answer.rstrip('#').split('#')  # 处理答案数据
    # print(answer)
    total, correct, wrong, correct_list, wrong_list= check_correct_num(answer)  # 检查答题情况
    
    # print(total)
    # print(correct)
    # print(wrong)
    # print(correct_list)
    # print(wrong_list)
    
    # return json_response(300, 'OK', {  # 返回JSON数据
    #     'qa_id': qa_id,
    #     'user_info': profile.data,
    #     'kind_id': kind_id,
    # })

    qa_info.aslogrecord = answer
    qa_info.correct_list = correct_list
    qa_info.wrong_list = wrong_list
    qa_info.finished_stamp = stop_stamp
    qa_info.expend_time = stop_stamp - qa_info.started_stamp
    qa_info.finished = True
    qa_info.correct_num = correct# if total == qa_info.total_num else 0
    qa_info.incorrect_num = wrong #if total == qa_info.total_num else qa_info.total_num
    qa_info.save()  # 保存答题log
    if qa_info.correct_num == kind_info.question_num:  # 得分处理
        score = kind_info.total_score
    elif not qa_info.correct_num:
        score = 0
    else:
        score = round((kind_info.total_score / kind_info.question_num) * correct, 3)
    qa_info.score = score  # 继续保存答题log
    qa_info.save()
    kind_info.total_partin_num += 1  # 保存比赛数据
    kind_info.save()  # 比赛答题次数
    bank_info.partin_num += 1
    bank_info.save()  # 题库答题次数
    if (kind_info.period_time > 0) and (qa_info.expend_time > kind_info.period_time * 60 * 1000):  # 超时，不加入排行榜
        qa_info.status = CompetitionQAInfo.OVERTIME
        qa_info.save()
    else:  # 正常完成，加入排行榜
        # add_to_rank(uid, kind_id, qa_info.score, qa_info.expend_time, qa_info.qa_id)
        qa_info.status = CompetitionQAInfo.COMPLETED
        qa_info.save()
    return json_response(200, 'OK', {  # 返回JSON数据
        'qa_id': qa_id,
        'user_info': profile.data,
        'kind_id': kind_id,
    })


@csrf_exempt
@check_login
@check_copstatus
@transaction.atomic
def userinfo_entry(request):
    """
    用户表单提交接口
    :param request: 请求对象
    :return: 返回json数据: user_info: 用户信息; kind_info: 比赛信息
    """

    uid = request.POST.get('uid', '')
    kind_id = request.POST.get('kind_id', '')
    result = request.POST.get('result', '')

    try:
        profile = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        return json_response(*ProfileError.ProfileNotFound)

    try:
        kind_info = CompetitionKindInfo.objects.get(kind_id=kind_id)
    except CompetitionKindInfo.DoesNotExist:
        return json_response(*CompetitionError.CompetitionNotFound)

    rl = [i.split(',') for i in result.rstrip('#').split('#')]

    ui, _ = UserInfo.objects.select_for_update().get_or_create(
        uid=uid,
        kind_id=kind_id
    )

    for i in rl:
        if hasattr(UserInfo, i[0]):
            setattr(ui, i[0], i[1])
    ui.save()

    enter_userinfo(kind_id, uid)

    return json_response(200, 'OK', {
        'user_info': profile.data,
        'kind_info': kind_info.data
    })




@csrf_exempt
def games(request, s):
    """
    获取所有比赛接口
    :param request: 请求对象
    :param s: 请求关键字
    :return: 返回该请求关键字对应的所有比赛类别
    """

    if s == 'hot':
        # 筛选条件: 完成时间大于当前时间;根据参与人数降序排序;根据创建时间降序排序;筛选10个
        kinds = CompetitionKindInfo.objects.filter(
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc),
        ).order_by('-total_partin_num').order_by('-created_at')[:10]

    elif s == 'tech':
        kinds = CompetitionKindInfo.objects.filter(
            sponsor_name=CompetitionKindInfo.INFECTION,
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).order_by('-total_partin_num').order_by('-created_at')

    elif s == 'edu':
        kinds = CompetitionKindInfo.objects.filter(
            sponsor_name=CompetitionKindInfo.EDUCATION,
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).order_by('-total_partin_num').order_by('-created_at')

    elif s == 'culture':
        kinds = CompetitionKindInfo.objects.filter(
            sponsor_name=CompetitionKindInfo.CULTURE,
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).order_by('-total_partin_num').order_by('-created_at')

    elif s == 'sport':
        kinds = CompetitionKindInfo.objects.filter(
            sponsor_name=CompetitionKindInfo.SPORT,
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).order_by('-total_partin_num').order_by('-created_at')

    elif s == 'general':
        kinds = CompetitionKindInfo.objects.filter(
            sponsor_name=CompetitionKindInfo.GENERAL,
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).order_by('-total_partin_num').order_by('-created_at')

    elif s == 'interview':
        kinds = CompetitionKindInfo.objects.filter(
            sponsor_name=CompetitionKindInfo.INTERVIEW,
            cop_finishat__gt=datetime.datetime.now(tz=datetime.timezone.utc)
        ).order_by('-total_partin_num').order_by('-created_at')

    else:
        kinds = None

    uid = request.session.get('uid', '')
    return json_response(200, 'OK', {
        'kinds': [i.data for i in kinds],
        'uid'  : uid
    })

@check_login
def qa_history_data(request):
    qaData = []
    try:
        qaInfos = CompetitionQAInfo.objects.filter(finished = 1).order_by('-finished_stamp')
    except CompetitionQAInfo.DoesNotExist:
        return render(request, 'err.html', CompetitionNotFound)

    for qainfo in qaInfos:
        os.environ["TZ"] = "UTC"
        # finished_time = datetime.datetime.fromtimestamp(qainfo.finished_stamp / 1e3).strftime("%Y/%m/%d %H:%M")
        finished_time = datetime.datetime.fromtimestamp(qainfo.finished_stamp / 1e3).strftime("%Y/%m/%d")
        try:
            kind_info = CompetitionKindInfo.objects.get(kind_id=qainfo.data["kind_id"])
            profile = Profile.objects.get(uid=qainfo.data["uid"])
            tTime = int(round(qainfo.detail["time"]))
            
            if tTime < 60:
                tTime = str(tTime) + "s"
            else:
                tTime = str(int(tTime / 60)) + "min"

            qaData.append({"name": profile.data["displayname"],
                "uid": profile.data["uid"],
                "kind_name" : kind_info.data["kind_name"], 
                "kind_id": kind_info.data["kind_id"], 
                "qa_id": qainfo.data["qa_id"], 
                "sponsor_name": kind_info.get_sponsor_name_display(), 
                "total_num": qainfo.detail["total_num"], 
                "correct_num": qainfo.detail["correct_num"],
                "incorrect_num": qainfo.detail["incorrect_num"],
                'trainee_type': profile.get_trainee_type_display(),
                "score": qainfo.detail["score"],
                "time": tTime,
                # "time1": qainfo.detail["time"],
                "finished_time": finished_time,
                })
        except CompetitionKindInfo.DoesNotExist:
            return render(request, 'err.html', CompetitionNotFound)
    # print(qaData)
    return json_response(200, 'OK', {
        'qaData': qaData,
    })

