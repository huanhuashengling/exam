from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from shortuuidfield import ShortUUIDField
from utils.basemodels import CreateUpdateMixin, MediaMixin

# Create your models here.
class Document(models.Model):
    category_id = models.CharField(_(u'分类id'), max_length=32, blank=True, null=True, help_text=u'分类唯一标识')
    doc_name = models.CharField(_(u'文档名称'), max_length=200,help_text=u'文档名称')
    is_public = models.BooleanField(_(u'是否公开'), default=True,help_text=u'是否公开')
    file_type = models.CharField(_(u'文件类型'), max_length=200,help_text=u'文件类型')
    upload_date = models.DateTimeField(_(u'文档上传时间'), default=timezone.now, help_text=_(u'文档上传时间'))
    change_date = models.DateTimeField(_(u'文档更新时间'), default=timezone.now, help_text=_(u'文档更新时间'))

class DownloadLog(models.Model):
    doc_id = models.CharField(_(u'文档id'), max_length=32, help_text=u'文档唯一标识', db_index=True)
    user_id = models.CharField(_(u'用户id'), max_length=32, help_text=u'用户唯一标识', db_index=True)
    download_date = models.DateTimeField(_(u'文档下载时间'), default=timezone.now, help_text=_(u'文档下载时间'))

class Category(models.Model):
    category_name = models.CharField(_(u'栏目名称'), max_length=200,help_text=u'栏目名称')
    created_date = models.DateTimeField(_(u'栏目创建时间'), default=timezone.now, help_text=_(u'栏目创建时间'))