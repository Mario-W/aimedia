# Generated by Django 2.0.4 on 2018-04-12 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame_number', models.IntegerField(default=0, verbose_name='图片序号')),
                ('frame_word', models.TextField(blank=True, null=True, verbose_name='图片字幕')),
                ('face_num', models.TextField(blank=True, null=True, verbose_name='人脸图片')),
            ],
        ),
        migrations.DeleteModel(
            name='Picture',
        ),
    ]
