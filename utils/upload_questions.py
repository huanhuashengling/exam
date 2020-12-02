import xlrd  # xlrd库
from django.db import transaction  # 数据库事物
from competition.models import ChoiceInfo, FillInBlankInfo, Subject, QuestionGroupInfo  # 题目数据模型
from django.db.models import Q

def check_vals(val):  # 检查值是否被转换成float，如果是，将.0结尾去掉
    val = str(val)
    if val.endswith('.0'):
        val = val[:-2]
    return val

def check_subject_vals(val):  # 匹配科目类型，是否需要匹配科室？
    val = check_vals(val)
    try:
        subject = Subject.objects.filter(Q(subject_name=val) | Q(subject_name_abb=val)).first()
    except Subject.DoesNotExist:
        return 0
    # print(val)
    return subject.id

@transaction.atomic
def upload_questions(file_path=None, bank_info=None):
    book = xlrd.open_workbook(file_path)  # 读取文件
    table = book.sheets()[0]  # 获取第一张表
    nrows = table.nrows  # 获取行数
    A1_choice_num = 0  # 选择题数量
    A2_choice_num = 0  # 选择题数量
    A3_choice_num = 0  # 选择题数量
    B_choice_num = 0  # 选择题数量
    G_fillinblank_num = 0  # 填空题数量
    for i in range(1, nrows):
        rvalues = table.row_values(i)  # 获取行中的值
        if (not rvalues[0]) or rvalues[0].startswith('说明'):  # 取出多余行
            break

        subjectId=check_subject_vals(rvalues[0])
        if 0 == subjectId:
            return "subject not found", "subject not found" 

        if '##' in rvalues[0]:  # 选择题 如果已经存在完全相同的题就不创建
            FillInBlankInfo.objects.select_for_update().create(
                bank_id=bank_info.bank_id,
                subject_id=subjectId,
                question=check_vals(rvalues[1]),
                answer=check_vals(rvalues[2]),
                # image_url=rvalues[4],
                source=rvalues[5]
            )
            G_fillinblank_num += 1  # 填空题数加1
        else:  # 填空题 如果已经存在完全相同的题就不创建
            tcode = check_vals(rvalues[1])
            codeArr = tcode.split("-")
            # print(tcode)
            if 1 == len(codeArr):
                ctype = tcode
                if "A1" == ctype:
                    A1_choice_num += 1
                    ctype = 1
                elif "A2" == ctype:
                    A2_choice_num += 1
                    ctype = 2

                question_group_order=0
                question_group_id=0

            elif 3 == len(codeArr):
                group_question_code = codeArr[0] + "_" + codeArr[1] + "_" + bank_info.bank_id
                question_group_order=codeArr[2]
                group_question_txt=check_vals(rvalues[2])

                oldQuestionGroupInfo = QuestionGroupInfo.objects.filter(group_question_code=group_question_code).first()
                if oldQuestionGroupInfo:
                    question_group_id=oldQuestionGroupInfo.id
                    oldQuestionGroupInfo.group_question_count += 1
                    oldQuestionGroupInfo.save()
                else:
                    if "A3" == codeArr[0]:
                        question_group_type = 1
                        ctype = 3
                        A3_choice_num += 1
                    elif "B" == codeArr[0]:
                        question_group_type = 2
                        B_choice_num += 1
                        ctype = 4
                    newQuestionGroupInfo = QuestionGroupInfo.objects.select_for_update().create(
                        question_group_type=question_group_type,
                        bank_id=bank_info.bank_id,
                        group_question_code=group_question_code,
                        group_question_txt=group_question_txt,
                        group_question_count=1,
                        )
                    question_group_id=newQuestionGroupInfo.id

            ChoiceInfo.objects.select_for_update().create(
                bank_id=bank_info.bank_id,
                subject_id=subjectId,
                ctype=ctype,
                question=check_vals(rvalues[4]),
                answer=check_vals(rvalues[6]),
                select_items=check_vals(rvalues[7]),
                source=check_vals(rvalues[3]),

                expound=check_vals(rvalues[8]),
                question_group_id= question_group_id,
                question_group_order=question_group_order,
                # image_url='',
            )
    bank_info.A1_choice_num = A1_choice_num
    bank_info.A2_choice_num = A2_choice_num
    bank_info.A3_choice_num = A3_choice_num
    bank_info.B_choice_num = B_choice_num
    bank_info.G_fillinblank_num = G_fillinblank_num
    bank_info.save()
    # print(A1_choice_num)
    # print(A2_choice_num)
    # print(A3_choice_num)
    # print(B_choice_num)
    return A1_choice_num, A2_choice_num, A3_choice_num, B_choice_num, G_fillinblank_num
