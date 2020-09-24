# Generated by Django 2.2.15 on 2020-09-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0006_auto_20180416_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=True, help_text='状态', verbose_name='状态')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('department_name', models.IntegerField(choices=[(0, '感染科'), (1, '内科'), (2, '外科'), (3, '儿科'), (4, '妇科')], default=0, help_text='科室类别', verbose_name='科室类别')),
            ],
            options={
                'verbose_name': '科室',
                'verbose_name_plural': '科室',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=True, help_text='状态', verbose_name='状态')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('department_id', models.CharField(blank=True, db_index=True, help_text='科室唯一标识', max_length=32, null=True, verbose_name='科室id')),
                ('subject_name_add', models.CharField(blank=True, help_text='科目所属缩写', max_length=255, null=True, verbose_name='科目所属缩写')),
                ('subject_name', models.CharField(blank=True, help_text='科目所属全称', max_length=255, null=True, verbose_name='科目所属全称')),
            ],
            options={
                'verbose_name': '科目',
                'verbose_name_plural': '科目',
            },
        ),
        migrations.RemoveField(
            model_name='choiceinfo',
            name='item1',
        ),
        migrations.RemoveField(
            model_name='choiceinfo',
            name='item2',
        ),
        migrations.RemoveField(
            model_name='choiceinfo',
            name='item3',
        ),
        migrations.RemoveField(
            model_name='choiceinfo',
            name='item4',
        ),
        migrations.AddField(
            model_name='choiceinfo',
            name='subject_id',
            field=models.CharField(blank=True, db_index=True, help_text='科目唯一标识', max_length=32, null=True, verbose_name='科目id'),
        ),
        migrations.AddField(
            model_name='fillinblankinfo',
            name='subject_id',
            field=models.CharField(blank=True, db_index=True, help_text='科目唯一标识', max_length=32, null=True, verbose_name='科目id'),
        ),
        migrations.AlterField(
            model_name='bankinfo',
            name='bank_type',
            field=models.IntegerField(choices=[(0, '感染科'), (1, '内科'), (2, '外科'), (3, '儿科'), (4, '妇科')], default=0, help_text='题库类型', verbose_name='题库类型'),
        ),
        migrations.AlterField(
            model_name='choiceinfo',
            name='question',
            field=models.CharField(blank=True, help_text='题目', max_length=1000, null=True, verbose_name='问题'),
        ),
        migrations.AlterField(
            model_name='competitionkindinfo',
            name='kind_type',
            field=models.IntegerField(choices=[(0, '感染科'), (1, '内科'), (2, '外科'), (3, '儿科'), (4, '妇科')], default=0, help_text='比赛类型', verbose_name='比赛类型'),
        ),
        migrations.AlterField(
            model_name='fillinblankinfo',
            name='question',
            field=models.CharField(blank=True, help_text='题目', max_length=1000, null=True, verbose_name='问题'),
        ),
    ]
