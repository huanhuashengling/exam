# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from shortuuidfield import ShortUUIDField
from utils.basemodels import CreateUpdateMixin, MediaMixin


class CompetitionKindInfo(CreateUpdateMixin):
    """试题类型信息类"""
    INFECTION = 0 #感染科
    INTERNAL = 1 #内科
    SURGICAL = 2 #外科
    PEDIATRIC = 3 #儿科
    GYNECOLOGY = 4 #妇科

    DAILY_PRACTICE = 0
    OUT_TEST = 1

    KIND_TYPES = (
        (DAILY_PRACTICE, u'日常练习'),
        (OUT_TEST, u'出科测试'),
    )

    SPONSOR_NAMES = (
        (INFECTION, u'感染科'),
        (INTERNAL, u'内科'),
        (SURGICAL, u'外科'),
        (PEDIATRIC, u'儿科'),
        (GYNECOLOGY, u'妇科'),
    )

    kind_id = ShortUUIDField(_(u'测试id'), max_length=32, blank=True, null=True, help_text=u'测试类别唯一标识', db_index=True)
    account_id = models.CharField(_(u'出题账户id'), max_length=32, blank=True, null=True, help_text=u'商家账户唯一标识', db_index=True)
    app_id = models.CharField(_(u'应用id'), max_length=32, blank=True, null=True, help_text=u'应用唯一标识', db_index=True)
    bank_id = models.CharField(_(u'题库id'), max_length=32, blank=True, null=True, help_text=u'题库唯一标识', db_index=True)
    kind_type = models.IntegerField(_(u'测试类别'), default=DAILY_PRACTICE, choices=KIND_TYPES, help_text=u'测试类别')
    kind_name = models.CharField(_(u'测试名称'), max_length=32, blank=True, null=True, help_text=u'测试名称')

    sponsor_name = models.IntegerField(_(u'出题科室'), default=INFECTION, choices=SPONSOR_NAMES, help_text=u'出题科室')

    total_score = models.IntegerField(_(u'总分数'), default=0, help_text=u'总分数')
    question_num = models.IntegerField(_(u'题目个数'), default=0, help_text=u'出题数量')
    A1_choice_num = models.IntegerField(_(u'A1型选择题数'), default=0, help_text=u'A1型选择题数')
    A2_choice_num = models.IntegerField(_(u'A2型选择题数'), default=0, help_text=u'A2型选择题数')
    A3_choice_num = models.IntegerField(_(u'A3型选择题数'), default=0, help_text=u'A3型选择题数')
    B_choice_num = models.IntegerField(_(u'B型选择题数'), default=0, help_text=u'B型选择题数')
    G_fillinblank_num = models.IntegerField(_(u'名词解释题数'), default=0, help_text=u'名词解释题数')
    EG_fillinblank_num = models.IntegerField(_(u'英语名词解释题数'), default=0, help_text=u'英语名词解释题数')
    S_fillinblank_num = models.IntegerField(_(u'简答题数'), default=0, help_text=u'简答题数')
    A_fillinblank_num = models.IntegerField(_(u'综合分析题数'), default=0, help_text=u'综合分析题数')
    # 周期相关
    cop_startat = models.DateTimeField(_(u'测试开始时间'), default=timezone.now, help_text=_(u'测试开始时间'))
    period_time = models.IntegerField(_(u'答题时间'), default=60, help_text=u'答题时间(min)')
    cop_finishat = models.DateTimeField(_(u'测试结束时间'), blank=True, null=True, help_text=_(u'测试结束时间'))

    # 参与相关
    total_partin_num = models.IntegerField(_(u'total_partin_num'), default=0, help_text=u'总参与人数')

    is_open = models.BooleanField(_(u'展示用户表单'), default=False, help_text=u'是否展示用户信息表单')

    class Meta:
        verbose_name = _(u'测试类别信息')
        verbose_name_plural = _(u'测试类别信息')

    def __unicode__(self):
        return str(self.pk)

    @property
    def data(self):
        return {
            'account_id': self.account_id,
            'app_id': self.app_id,
            'kind_id': self.kind_id,
            'kind_type': self.kind_type,
            'kind_name': self.kind_name,
            'total_score': self.total_score,
            'question_num': self.question_num,
            'A1_choice_num': self.A1_choice_num,
            'A2_choice_num': self.A2_choice_num,
            'A3_choice_num': self.A3_choice_num,
            'B_choice_num': self.B_choice_num,
            'G_fillinblank_num': self.G_fillinblank_num,
            'EG_fillinblank_num': self.EG_fillinblank_num,
            'S_fillinblank_num': self.S_fillinblank_num,
            'A_fillinblank_num': self.A_fillinblank_num,
            'total_partin_num': self.total_partin_num,
            'cop_startat': self.cop_startat,
            'cop_finishat': self.cop_finishat,
            'period_time': self.period_time,
            'sponsor_name': self.sponsor_name,
            'is_open': self.is_open,
        }


class BankInfo(CreateUpdateMixin):
    """
    题库信息类
    """
    INFECTION = 0 #感染科
    INTERNAL = 1 #内科
    SURGICAL = 2 #外科
    PEDIATRIC = 3 #儿科
    GYNECOLOGY = 4 #妇科

    BANK_TYPES = (
        (INFECTION, u'感染科'),
        (INTERNAL, u'内科'),
        (SURGICAL, u'外科'),
        (PEDIATRIC, u'儿科'),
        (GYNECOLOGY, u'妇科'),
    )

    bank_id = ShortUUIDField(_(u'题库id'), max_length=32, blank=True, null=True, help_text=u'题库唯一标识', db_index=True)
    uid = models.CharField(_(u'用户id'), max_length=32, blank=True, null=True, help_text=u'用户唯一标识', db_index=True)
    account_id = models.CharField(_(u'商家id'), max_length=32, blank=True, null=True, help_text=u'商家账户唯一标识', db_index=True)
    bank_name = models.CharField(_(u'题库名称'), max_length=40, blank=True, null=True, help_text=u'题库名称')

    A1_choice_num = models.IntegerField(_(u'A1型选择题数'), default=0, help_text=u'A1型选择题数')
    A2_choice_num = models.IntegerField(_(u'A2型选择题数'), default=0, help_text=u'A2型选择题数')
    A3_choice_num = models.IntegerField(_(u'A3型选择题数'), default=0, help_text=u'A3型选择题数')
    B_choice_num = models.IntegerField(_(u'B型选择题数'), default=0, help_text=u'B型选择题数')
    G_fillinblank_num = models.IntegerField(_(u'名词解释题数'), default=0, help_text=u'名词解释题数')
    EG_fillinblank_num = models.IntegerField(_(u'英语名词解释题数'), default=0, help_text=u'英语名词解释题数')
    S_fillinblank_num = models.IntegerField(_(u'简答题数'), default=0, help_text=u'简答题数')
    A_fillinblank_num = models.IntegerField(_(u'综合分析题数'), default=0, help_text=u'综合分析题数')
    bank_type = models.IntegerField(_(u'题库类型'), default=INFECTION, choices=BANK_TYPES, help_text=u'题库类型')
    kind_num = models.IntegerField(_(u'测试使用次数'), default=0, help_text=u'测试使用次数')
    partin_num = models.IntegerField(_(u'总答题人数'), default=0, help_text=u'总答题人数')

    class Meta:
        verbose_name = _(u'题库')
        verbose_name_plural = _(u'题库')

    def __unicode__(self):
        return str(self.pk)

    @property
    def total_question_num(self):
        return self.A1_choice_num + self.A2_choice_num + self.A3_choice_num + self.B_choice_num + self.G_fillinblank_num + self.EG_fillinblank_num + self.S_fillinblank_num + self.A_fillinblank_num

    @property
    def data(self):
        return {
            'bank_id': self.bank_id,
            'bank_name': self.bank_name,
            'A1_choice_num': self.A1_choice_num,
            'A2_choice_num': self.A2_choice_num,
            'A3_choice_num': self.A3_choice_num,
            'B_choice_num': self.B_choice_num,
            'G_fillinblank_num': self.G_fillinblank_num,
            'EG_fillinblank_num': self.EG_fillinblank_num,
            'S_fillinblank_num': self.S_fillinblank_num,
            'A_fillinblank_num': self.A_fillinblank_num,
            'bank_type': dict(self.BANK_TYPES)[self.bank_type],
            'kind_num': self.kind_num,
            'partin_num': self.partin_num,
            'total_question_num': self.total_question_num
        }


class ChoiceInfo(CreateUpdateMixin):
    QUESTION_TYPE = 'choice'

    A1 = 1
    A2 = 2
    A3 = 3
    B = 4
    # C = 5
    # MULTI = 6
    

    CHOICE_TYPE = (
        (A1, u'概念单选'),
        (A2, u'分析单选'),
        (A3, u'共题干分析单选'),
        (B, u'共答案单选'),
        # (C, u'共答案单选'),
        # (MULTI, u'多选题'),
    )

    bank_id = models.CharField(_(u'题库id'), max_length=32, blank=True, null=True, help_text=u'题库唯一标识', db_index=True)
    subject_id = models.CharField(_(u'科目id'), max_length=32, blank=True, null=True, help_text=u'科目唯一标识', db_index=True)
    ctype = models.IntegerField(_(u'选择题类型'), choices=CHOICE_TYPE, default=A1, help_text=u'选择题类型')
    question = models.CharField(_(u'问题'), max_length=1000, blank=True, null=True, help_text=u'题目')
    answer = models.CharField(_(u'答案'), max_length=255, blank=True, null=True, help_text=u'答案')
    select_items = models.CharField(_(u'选项'), max_length=2000, blank=True, null=True, help_text=u'选项文本')
    
    source = models.CharField(_(u'出题处'), max_length=255, blank=True, null=True, help_text=u'出提处')
    expound = models.CharField(_(u'解析'), max_length=1000, blank=True, null=True, help_text=u'解析')
    question_group_id = models.CharField(_(u'题组id'), max_length=32, blank=True, null=True, help_text=u'题组', db_index=True)
    question_group_order = models.IntegerField(_(u'题组中序号'), default=0, help_text=u'题组中序号')

    class Meta:
        verbose_name = _(u'选择题')
        verbose_name_plural = _(u'选择题')

    def __unicode__(self):
        return str(self.pk)

    @property
    def items(self):
        return self.select_items

    @property
    def data_without_answer(self):
        return {
            'pk': self.pk,
            'qtype': self.QUESTION_TYPE,
            'bank_id': self.bank_id,
            'ctype': self.ctype,
            'question': self.question,
            'items': self.select_items,
            'source': self.source,
            'expound': self.expound,
            'question_group_id': self.question_group_id,
            'question_group_order': self.question_group_order,
        }

    @property
    def data(self):
        return {
            'pk': self.pk,
            'qtype': self.QUESTION_TYPE,
            'bank_id': self.bank_id,
            'ctype': self.ctype,
            'question': self.question,
            'answer': self.answer,
            'items': self.select_items,
            'source': self.source,
            'expound': self.expound,
            'question_group_id': self.question_group_id,
            'question_group_order': self.question_group_order,
        }

class QuestionGroupInfo(CreateUpdateMixin):

    QUESTION_TYPE = 'question_group'

    A3 = 1
    B = 2
    ANALYSIS = 3

    QUESTION_GROUP_TYPE = (
        (A3, u'共题干分析单选'),
        (B, u'共答案单选'),
        (ANALYSIS, u'案例分析题'),
    )

    bank_id = models.CharField(_(u'题库id'), max_length=32, blank=True, null=True, help_text=u'题库唯一标识', db_index=True)
    group_question_txt = models.CharField(_(u'组题干'), max_length=1000, blank=True, null=True, help_text=u'组题干')
    group_question_count = models.IntegerField(_(u'题组中题数'), default=0, help_text=u'题组中题数')
    group_question_code = models.CharField(_(u'题组编号'), max_length=100, blank=True, null=True, help_text=u'题组编号')
    question_group_type = models.IntegerField(_(u'组题类型'), choices=QUESTION_GROUP_TYPE, default=A3, help_text=u'组题类型')

    class Meta:
        verbose_name = _(u'题组')
        verbose_name_plural = _(u'题组')

    def __unicode__(self):
        return str(self.pk)

    @property
    def data(self):
        return {
            'pk': self.pk,
            'qtype': self.QUESTION_TYPE,
            'bank_id': self.bank_id,
            'question_group_type': self.question_group_type,
            'group_question_txt': self.group_question_txt,
            'group_question_code': self.group_question_code,
            'group_question_count': self.group_question_count,
        }

class FillInBlankInfo(CreateUpdateMixin):
    """
    填空题信息类
    """

    QUESTION_TYPE = 'fillinblank'


    GLOSSARY = 1
    EGLOSSARY = 2
    SHORT = 3
    ANALYSIS = 4

    FILLBLANK_TYPE = (
        (GLOSSARY, u'名词解释'),
        (EGLOSSARY, u'英语名词解释'),
        (SHORT, u'简答题'),
        (ANALYSIS, u'案例分析题'),
    )

    bank_id = models.CharField(_(u'题库id'), max_length=32, blank=True, null=True, help_text=u'题库唯一标识', db_index=True)
    subject_id = models.CharField(_(u'科目id'), max_length=32, blank=True, null=True, help_text=u'科目唯一标识', db_index=True)
    ftype = models.IntegerField(_(u'填空类型'), choices=FILLBLANK_TYPE, default=GLOSSARY, help_text=u'填空类型')
    question = models.CharField(_(u'问题'), max_length=1000, blank=True, null=True, help_text=u'题目')
    answer = models.CharField(_(u'答案'), max_length=255, blank=True, null=True, help_text=u'答案')
    
    source = models.CharField(_(u'出题处'), max_length=255, blank=True, null=True, help_text=u'出题处')
    question_group_id = models.CharField(_(u'题组id'), max_length=32, blank=True, null=True, help_text=u'题组', db_index=True)
    question_group_order = models.IntegerField(_(u'题组中序号'), default=0, help_text=u'题组中序号')

    class Meta:
        verbose_name = _(u'填空题')
        verbose_name_plural = _(u'填空题')

    def __unicode__(self):
        return str(self.pk)

    @property
    def data_without_answer(self):
        return {
            'pk': self.pk,
            'bank_id': self.bank_id,
            'ftype': self.ftype,
            'question': self.question,
            'qtype': self.QUESTION_TYPE,
            'source': self.source
        }

    @property
    def data(self):
        return {
            'pk': self.pk,
            'bank_id': self.bank_id,
            'ftype': self.ftype,
            'question': self.question,
            'qtype': self.QUESTION_TYPE,
            'answer': self.answer,
            'source': self.source
        }


class CompetitionQAInfo(CreateUpdateMixin):
    """答题记录信息类"""

    UNCOMPLETED = 0
    COMPLETED = 1
    OVERTIME = 2

    STATUS_CHOICES = (
        (UNCOMPLETED, u'未完成'),
        (COMPLETED, u'已完成'),
        (OVERTIME, u'超时')
    )

    status = models.IntegerField(_(u'答题状态'), choices=STATUS_CHOICES, default=0, help_text=u'答题状态')
    kind_id = models.CharField(_(u'测试id'), max_length=32, blank=True, null=True, help_text=u'测试类别唯一标识', db_index=True)
    qa_id = ShortUUIDField(_(u'问题id'), max_length=32, blank=True, null=True, help_text=u'QA 唯一标识', db_index=True)
    uid = models.CharField(_(u'用户id'), max_length=32, blank=True, null=True, help_text=u'用户唯一标识', db_index=True)

    # 问题答案相关
    qsrecord = models.TextField(_('问题记录'), max_length=10000, blank=True, null=True, help_text=u'问题记录')
    asrecord = models.TextField(_('答案记录'), max_length=10000, blank=True, null=True, help_text=u'答案记录')
    aslogrecord = models.TextField(_('答案提交记录'), max_length=10000, blank=True, null=True, help_text=u'答案提交记录')

    # 耗费时间相关
    started_stamp = models.BigIntegerField(_(u'开始时间戳'), default=0, help_text=u'开始时间戳(毫秒)')
    finished_stamp = models.BigIntegerField(_(u'结束时间戳'), default=0, help_text=u'结束时间戳(毫秒)')
    expend_time = models.IntegerField(_(u'耗时'), default=0, help_text=u'耗费时间(毫秒)')

    started = models.BooleanField(_(u'已开始'), default=False, help_text=u'是否开始', db_index=True)
    finished = models.BooleanField(_(u'已结束'), default=False, help_text=u'是否结束', db_index=True)

    # 得分相关
    correct_num = models.IntegerField(_(u'正确数'), default=0, help_text=u'答对数量')
    incorrect_num = models.IntegerField(_(u'错误数'), default=0, help_text=u'答错数量')
    correct_list = models.CharField(_(u'正确答案列表'), max_length=10000, blank=True, null=True, help_text=u'正确答案列表')
    wrong_list = models.CharField(_(u'错误答案列表'), max_length=10000, blank=True, null=True, help_text=u'错误答案列表')
    total_num = models.IntegerField(_(u'总数'), default=0, help_text=u'总共数量')
    score = models.FloatField(_(u'得分'), default=0, help_text=u'分数')

    class Meta:
        verbose_name = _(u'测试问题记录')
        verbose_name_plural = _(u'测试问题记录')

    def __unicode__(self):
        return str(self.pk)

    @property
    def data(self):
        return {
            'qa_id': self.qa_id,
            'kind_id': self.kind_id,
            'uid': self.uid,
        }

    @property
    def detail(self):
        return {
            'status': self.status,
            'qa_id': self.qa_id,
            'qs': self.qsrecord,
            'as': self.asrecord,
            'aslog': self.aslogrecord,
            'total_num': self.total_num,
            'correct_num': self.correct_num,
            'incorrect_num': self.incorrect_num,
            'correct_list': self.correct_list,
            'wrong_list': self.wrong_list,
            'score': self.score,
            'time': self.expend_time / 1000.000,
        }

class Department(CreateUpdateMixin):
    INFECTION = 0 #感染科
    INTERNAL = 1 #内科
    SURGICAL = 2 #外科
    PEDIATRIC = 3 #儿科
    GYNECOLOGY = 4 #妇科

    DEPARTMENT_CHOICES = (
        (INFECTION, u'感染科'),
        (INTERNAL, u'内科'),
        (SURGICAL, u'外科'),
        (PEDIATRIC, u'儿科'),
        (GYNECOLOGY, u'妇科'),
    )

    department_name = models.IntegerField(_(u'科室类别'), choices=DEPARTMENT_CHOICES, default=0, help_text=u'科室类别')

    class Meta:
        verbose_name = _(u'科室')
        verbose_name_plural = _(u'科室')

    def __unicode__(self):
        return str(self.pk)

class Subject(CreateUpdateMixin):
    department_id = models.CharField(_(u'科室id'), max_length=32, blank=True, null=True, help_text=u'科室唯一标识', db_index=True)
    subject_name_abb = models.CharField(_(u'科目所属缩写'), max_length=255, blank=True, null=True, help_text=u'科目所属缩写')
    subject_name = models.CharField(_(u'科目所属全称'), max_length=255, blank=True, null=True, help_text=u'科目所属全称')
    index_order = models.IntegerField(_(u'索引编号'), default=0, help_text=u'索引编号')
    item_order = models.IntegerField(_(u'单项编号'), default=0, help_text=u'单项编号')

    class Meta:
        verbose_name = _(u'科目')
        verbose_name_plural = _(u'科目')

    def __unicode__(self):
        return str(self.pk)
