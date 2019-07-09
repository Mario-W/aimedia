import sys,os
sys.path.append('../../aimedia')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','aimedia.settings')
import django
django.setup()
from aimedia import settings
from media.models import *
scene = Scene(scene_name = 'iitest')
scene.save()
scenes = Scene.objects.all()
print(len(scenes))

program = Program.objects.get(id=1)
print(program.picture_names[2])
