import xlrd  # xlrd库
from django.db import transaction  # 数据库事物
from competition.models import ChoiceInfo, FillInBlankInfo, Subject  # 题目数据模型
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
    return subject.id

@transaction.atomic
def upload_questions(file_path=None, bank_info=None):
    book = xlrd.open_workbook(file_path)  # 读取文件
    table = book.sheets()[0]  # 获取第一张表
    nrows = table.nrows  # 获取行数
    choice_num = 0  # 选择题数量
    fillinblank_num = 0  # 填空题数量
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
                subject_id=check_subject_vals(rvalues[0]),
                question=check_vals(rvalues[1]),
                answer=check_vals(rvalues[2]),
                image_url=rvalues[4],
                source=rvalues[5]
            )
            fillinblank_num += 1  # 填空题数加1
        else:  # 填空题 如果已经存在完全相同的题就不创建
            ChoiceInfo.objects.select_for_update().create(
                bank_id=bank_info.bank_id,
                subject_id=check_subject_vals(rvalues[0]),
                question=check_vals(rvalues[1]),
                answer=check_vals(rvalues[3]),
                select_items=check_vals(rvalues[4]),
                # item1=check_vals(rvalues[2]),
                # item2=check_vals(rvalues[3]),
                # item3=check_vals(rvalues[4]),
                # item4=check_vals(rvalues[5]),
                image_url=rvalues[5],
                source=rvalues[6]
            )
            choice_num += 1  # 选择题数加1
    bank_info.choice_num = choice_num
    bank_info.fillinblank_num = fillinblank_num
    bank_info.save()
    return choice_num, fillinblank_num
