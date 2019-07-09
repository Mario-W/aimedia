#! /usr/local/bin/python3
# -*- coding=utf8 -*-
import os,sys
#sys.path.append('../../aimedia')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE','aimedia.settings')
#import django
#django.setup()



import os.path
import time
import datetime
import schedule
import glob
import requests
from pandas import json
from histsimilar import *
import face_recognition
from PIL import Image
import queue
import threading
import pytesseract
from django import db
import shutil

#setup django models 
sys.path.append('../../aimedia')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','aimedia.settings')
import django
django.setup()
from aimedia import settings
from media.models import *


basedir = os.getcwd()
mediadir=basedir + "/media"
text_rec_url =  'http://101.132.103.213/upload/'





picmergequeue = queue.Queue()
facerecqueue = queue.Queue()
scenequeue = queue.Queue()
textrecqueue = queue.Queue()
programsplitqueue = queue.Queue()
programdog = queue.Queue()

class ThreadPicMerge(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue =queue

    def run(self):
        while True:
            scenepath =self.queue.get()
            if scenepath:
                print("merge thread "+scenepath)
                program_name = scenepath.split('/')[-2]
                series_name = scenepath.split('/')[-3]
                program_key_frame = series_name+'-'+program_name+'-keyframe.mp4'
                merge_cmd = "cd "+scenepath+"; " +"ffmpeg -y -r 1 -pattern_type glob -i './*.jpg' -vcodec mpeg4 "+program_key_frame + " 2>>ffmpag.log"
                os.system(merge_cmd)
            time.sleep(5)

class ThreadFaceRec(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue =queue

    def run(self):
        while True:
            iface=[]
            picpath =self.queue.get()
            if picpath:
                program_name = picpath.split('/')[-1]
                series_name = picpath.split('/')[-2]

                picfiles = glob.glob(picpath+'/scene/'+'*.jpg')
                print("pic file is %d"%len(picfiles))
                for pic in picfiles:
                
                    path,filename=os.path.split(pic);
                    picnum = int(filename.split('.')[0])
                    image = face_recognition.load_image_file(pic)
                    faces = face_recognition.face_locations(image)
                    for i in range(len(faces)):
                        face = Image.fromarray(image[faces[i][0]:faces[i][2],faces[i][3]:faces[i][1]])

                        facefile = picpath+'/faces'+"/"+str(picnum)+"-%d.jpg"%(i+1)
                        face.save(facefile)
                        iface.append((str(picnum)+'-%d')%(i+1))

            db.close_old_connections()
            programdb = Program.objects.filter(program_name=program_name,series_name=series_name)
            if programdb:
                programdb[0].face_num = iface
                programdb[0].save()

            time.sleep(2)


class ThreadScene(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue =queue

    def run(self):
        while True:
            db.close_old_connections()
            benchofsimilar = Parameter.objects.get(id=1).similar_bench
            picpath =self.queue.get()
            if picpath:
                program_name = picpath.split('/')[-1]
                series_name = picpath.split('/')[-2]
                picfiles = glob.glob(picpath+'/'+'*.jpg')
                picnum = []
                for pic in picfiles:
                    path,filename=os.path.split(pic);
                    picnum.append( int(filename.split('.')[0]))
                picnum.sort()
            
                
                file = picpath+'/'+str(1)+'.jpg'
                os.system('cp '+ file + ' ' +picpath+"/scene")
                picnum.remove(1)
                basefile = picpath+'/'+str(1)+'.jpg'
                seg_start_num = 1  
                img = Image.open(basefile)
                littleimg = img.resize((90,72))
                littleimg.save(picpath+'/scene/'+'1-l.png','png')
                
                first_frame = [1] 
                for i in picnum:
                    ifile = picpath+'/'+str(i)+'.jpg'
                    similar = calc_similar_by_path(basefile,ifile)
                    if similar*100 < benchofsimilar:
                        basefile = ifile
                        os.system('cp '+ ifile +' ' + picpath+"/scene")
                        first_frame.append(i)
                        img = Image.open(ifile)
                        littleimg = img.resize((90,72))
                        littleimg.save(picpath+'/scene/'+str(i)+'-l.png','png')
                        seg_end_num = i
                        db.close_old_connections()
                        segment = Segment(program_name = program_name,segment_start_num = seg_start_num,segment_end_num=seg_end_num)
                        segment.save()
                        seg_start_num = i

                print(first_frame)
                picmergequeue.put(picpath+'/scene')
                facerecqueue.put(picpath)

                db.close_old_connections()
                programdb = Program.objects.filter(program_name=program_name,series_name=series_name)
                if programdb:
                    programdb[0].segment_num = first_frame
                    programdb[0].similar_bench = benchofsimilar
                    programdb[0].save()

            time.sleep(2)


class ThreadTextRec1(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue =queue

    def run(self):
        while True:
            picpath =self.queue.get()
            if picpath:
                picfiles = glob.glob(picpath+'/'+'*.jpg')
                for pic in picfiles:
                    file  = pic
                    files = {'file':open(file,'rb')}
                    rs = requests.post(text_rec_url,files=files)
                    rj = rs.json()
                    print(rj)
                    #will be define
            
            time.sleep(2)


class ThreadTextRec(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue =queue

    def run(self):
        while True:
            picpath =self.queue.get()
            if picpath:
                program_name = picpath.split('/')[-1]
                series_name = picpath.split('/')[-2]
                picfiles = glob.glob(picpath+'/'+'*.jpg')
                ilist = []
                print(picfiles)
                for pic in picfiles:
                    frame_num = pic.split('/')[-1].split('.')[0]
                    img = Image.open(pic)
                    txt = pytesseract.image_to_string(img,lang='chi_sim').strip().replace("\n","")
                    print("rec text is :%s"%txt)
                    if txt:
                        ilist.append({'frame_num':frame_num, 'text': txt})

                db.close_old_connections()
                programdb = Program.objects.filter(series_name=series_name,program_name=program_name)
                if programdb:
                    programdb[0].frame_text = ilist
                    programdb[0].save()
            
            time.sleep(2)


class ThreadProgramSplit(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue =queue

    def run(self):
        while True:
            print('get a queue')
            a_program =self.queue.get()
            print(a_program)
            if a_program:
                program = a_program
            print('post get a queue')
            if program:
                print('get a split queue')
                filename = program.split('/')[-1]

                absfilename = filename.split('.')[0]
                
                picpath = os.path.dirname(program) + '/' + absfilename
                series_name  = picpath.split('/')[-2]
                scenepath = os.path.join(picpath,'scene')

                facespath = os.path.join(picpath,'faces')
                print(scenepath)
                print(facespath)
                os.mkdir(picpath)
                os.mkdir(scenepath)
                os.mkdir(facespath)

                db.close_old_connections()
                pps = Parameter.objects.get(id=1).frame_per_second

                splitcmd = "ffmpeg -ss 00:00 -i "+ program + " -f image2 -r " + str(pps) +" %d.jpg"
                mvpiccmd = "mv " + "./*.jpg " + picpath
                os.system(splitcmd+';'+ mvpiccmd)
                picfiles = glob.glob(picpath+'/'+'*.jpg')
                db.close_old_connections()
                program = Program(program_name = absfilename,series_name=series_name,frame_names = picfiles,fps_interval=pps)
                program.save()
            
                textrecqueue.put(picpath)
                scenequeue.put(picpath)
            



class ThreadProgramDog(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue =queue
        self.his_content = os.listdir(mediadir)
        self.newfilelist = []
        
    def run(self):
        while True:
            now_content = os.listdir(mediadir)
            print(now_content) 

            media_series = list(set(now_content).difference(set(self.his_content)))
            self.his_content = now_content
            for a_series in media_series:
                series_path = mediadir+'/'+a_series
                print(series_path)
                print(os.path.isdir(series_path))
                if os.path.isdir(series_path):
                    new_media = glob.glob(series_path+"/*.wmv")
                    new_media += glob.glob(series_path+"/*.mp4")
                    [programsplitqueue.put(program) for program in new_media]

#系列名称和类型已经在django中写入，此处不需要再写入
#                    db.close_old_connections()               
#                    series = Series(series_name = a_series,series_type = '综艺')
#                    series.save()
            time.sleep(10)




if len(Parameter.objects.all()) == 0:
    parameter = Parameter(file_check_interval = 10,frame_per_second = 1,similar_bench =55)
    parameter.save()





t1= ThreadPicMerge(picmergequeue)
t1.start()
t2= ThreadFaceRec(facerecqueue)
t2.start()
t3 = ThreadScene(scenequeue)
t3.start()
t4 = ThreadTextRec(textrecqueue)
t4.start()
t5 = ThreadProgramSplit(programsplitqueue)
t5.start()
t6 = ThreadProgramDog(programdog)
t6.start()

#media_process = MEDIA()







