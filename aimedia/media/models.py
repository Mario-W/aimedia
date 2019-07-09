#--*-- coding:utf8 --*--
from django.db import models


class Series(models.Model):
    series_name = models.CharField(verbose_name='系列名称', default='', max_length=100)
    surface_image = models.CharField(verbose_name='封面图片', default='', max_length=1024)
    series_type = models.CharField(verbose_name='系列类型', default='', max_length=32)
    nake_name = models.CharField(verbose_name='别名', default='', max_length=100)
    episodes_num = models.IntegerField(verbose_name='集数', default=1, max_length=100)
    series_keywords = models.CharField(verbose_name='关键词', default='', max_length=500)
    content_descript = models.CharField(verbose_name='描述', default='', max_length=500)
    key_person = models.CharField(verbose_name='描述', default='', max_length=500)
    taken_date = models.CharField(verbose_name='描述', default='', max_length=500)
    taken_place = models.CharField(verbose_name='描述', default='', max_length=500)
    award = models.CharField(verbose_name='描述', default='', max_length=500)
    audience = models.CharField(verbose_name='描述', default='', max_length=500)
    productor = models.CharField(verbose_name='描述', default='', max_length=500)
    publisher = models.CharField(verbose_name='描述', default='', max_length=500)
    language = models.CharField(verbose_name='描述', default='', max_length=500)
    version = models.CharField(verbose_name='描述', default='', max_length=500)
    source_type = models.CharField(verbose_name='描述', default='', max_length=500)
    source_privider = models.CharField(verbose_name='描述', default='', max_length=500)
    copy_right = models.CharField(verbose_name='描述', default='', max_length=500)
    start_time = models.CharField(verbose_name='描述', default='', max_length=500)
    right_area = models.CharField(verbose_name='描述', default='', max_length=500)
    use_times = models.CharField(verbose_name='描述', default='', max_length=500)
    right_others = models.CharField(verbose_name='描述', default='', max_length=500)


class Program(models.Model):
    program_name = models.CharField(verbose_name = '节目名称',default = '',max_length = 100)
    series_name = models.CharField(verbose_name = '系列名称',default = '',max_length = 100)
    order_index = models.IntegerField(verbose_name='排序序号', default=0)
    process_date=models.DateTimeField(verbose_name='处理时间', auto_now=True)
    fps_interval = models.IntegerField(verbose_name='每秒抽取帧数',default = 0)
    frame_names = models.TextField(verbose_name='图片文件名',blank=True,null=True)
    face_num = models.TextField(verbose_name='人脸图片',blank=True,null=True)
    segment_num = models.TextField(verbose_name = "场景第一帧",blank = True,null=True)
    similar_bench = models.IntegerField(verbose_name='相似度门限',default=50)
    frame_text = models.TextField(verbose_name='图片字幕',blank=True,null=True)


class Segment(models.Model):
    program_name = models.CharField(max_length = 100)
    series_name = models.CharField(verbose_name = '系列名称',default = '',max_length = 100)
    segmengt_keywords = models.CharField(max_length = 1000)
    segment_descript = models.TextField(verbose_name = "片段",blank=True,null=True)
    segment_start_num = models.IntegerField(verbose_name ='当前段结束帧', default=0)
    segment_end_num = models.IntegerField(verbose_name ='当前段结束帧', default=0)








'''

class Scene(models.Model):
    scene_name = models.CharField(max_length = 100)
    scene_keywords = models.CharField(verbose_name = "关键词",max_length = 1000)
    scene_descript = models.TextField(verbose_name = "场景",blank=True,null=True)
    similar_bench = models.IntegerField(verbose_name='相似度门限',default=50)
    first_frame = models.TextField(verbose_name = "场景第一帧",blank = True,null=True)

class Frame(models.Model):
    frame_path = models.CharField(verbose_name='图片路路径',default = '',max_length = 200)
    frame_text = models.TextField(verbose_name='图片字幕',blank=True,null=True)
    face_num = models.TextField(verbose_name='人脸图片',blank=True,null=True)
'''

class Parameter(models.Model):
    similar_bench = models.IntegerField(verbose_name='相似度门限',default=50)
    file_check_interval = models.IntegerField(verbose_name='新文件检测间隔',default=10)
    frame_per_second = models.IntegerField(verbose_name='抽帧频率（每秒抽多少帧）',default=2)




