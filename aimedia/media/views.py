import os
import shutil
import _datetime
from django.shortcuts import render
from django.http import JsonResponse
from media.models import Program, Segment, Series


# 根据系列名称返回本系列所有视频信息
def index(request):

    series_name = request.GET.get('series_name') or ''
    program_list = Program.objects.filter(series_name=series_name)

    series_obj_set = Series.objects.filter(series_name=series_name)

    media_path = ''

    segment_list = []
    head_list = []
    subtitle_list = []
    key_frame_list = []
    thumb_list = []

    process_date = ''
    first_segment_poster = ''


    segment_page_count = 1

    if program_list:
        first_program = program_list[0]
        media_path = os.path.join('/static', 'media', first_program.series_name, first_program.program_name + '.mp4')
        print('media_path is :{0},{1}'.format(media_path,first_program.series_name))
        head_filename_list = eval(first_program.face_num or '[]')
        head_list = [os.path.join('/static', 'media', first_program.series_name, first_program.program_name,
                                  'faces', head + '.jpg') for head in head_filename_list]
        
        print('head_filename_list is :{0}'.format(head_filename_list))
        subtitle_list = eval(first_program.frame_text or '[]')
        key_frame_filename_list = eval(first_program.segment_num or '[]')
        key_frame_list = [os.path.join('/static', 'media', first_program.series_name, first_program.program_name,
                                  'scene', str(frame) + '-l.png') for frame in key_frame_filename_list]
        segment_list = Segment.objects.filter(program_name=first_program.program_name, series_name=series_name)
        if segment_list:
            first_segment_poster = os.path.join('/static', 'media', first_program.series_name, first_program.program_name,
                                                str(segment_list[0].segment_start_num) + '.jpg')
            segment_page_count = int(segment_list.count()/4) + 1 if segment_list.count()/4 != 0 else int(segment_list.count()/4)

            for seg in segment_list:
                thumb_list.append({
                    'thumb': os.path.join('/static', 'media', first_program.series_name, first_program.program_name, 'scene',
                                       str(seg.segment_start_num) + '-l.png'),
                    'frame_id': seg.segment_start_num,
                    'program_name': seg.program_name,
                    'description': seg.segment_descript or '',
                    })

    return render(request, 'index.html', {
        'subtitle_list': subtitle_list,
        'media_path': media_path,
        'head_list': head_list,
        'key_frame_list': key_frame_list,   # 每个关键帧对应相应的播放时间
        'segment_page_count': segment_page_count,
        'page_index': 1,
        'program_list': program_list[:22],
        'segment_list': segment_list,
        'process_date': process_date,
        'first_segment_poster': first_segment_poster,
        'thumb_list': thumb_list,
        'program_name': program_list[0].program_name if program_list.count() > 0 else '',
        'series_name': series_name,
        'seires_obj': series_obj_set[0] if series_obj_set else {},
    })


# 根据每集名称返回本集视频信息
def get_program_info(request):

    series_name = request.GET.get('series_name')
    program_name = request.GET.get('program_name')
    program_set = Program.objects.filter(program_name=program_name, series_name=series_name)
    if not program_set:
        return JsonResponse({'res': 'error', 'msg': 'no program!'})

    program = program_set[0]

    media_path = os.path.join('/static', 'media', program.series_name, program.program_name + '.mp4')

    head_filename_list = eval(program.face_num or '[]')
    print(head_filename_list)
    head_list = [os.path.join('/static', 'media', program.series_name, program.program_name,
                              'faces', head + '.jpg') for head in head_filename_list]
    subtitle_list = eval(program.frame_text or '[]')
    key_frame_filename_list = eval(program.segment_num or '[]')
    key_frame_list = [os.path.join('/static', 'media', program.series_name, program.program_name,
                                   'scene', str(frame) + '-l.png') for frame in key_frame_filename_list]
    segment_set = Segment.objects.filter(program_name=program.program_name, series_name=series_name)
    segment_list = [seg.segment_start_num for seg in segment_set]

    first_segment_poster = ''
    segment_page_count = 1
    thumb_list = []

    if segment_list:
        first_segment_poster = os.path.join('/static', 'media', program.series_name, program.program_name,
                                            str(segment_set[0].segment_start_num) + '.jpg')
        segment_page_count = int(segment_set.count() / 4) + 1 if segment_set.count() / 4 != 0 else int(
            segment_set.count() / 4)

        for seg in segment_set:
            thumb_list.append({
                'thumb': os.path.join('/static', 'media', seg.series_name, seg.program_name, 'scene',
                                   str(seg.segment_start_num) + '-l.png'),
                'frame_id': seg.segment_start_num,
                'program_name': seg.program_name,
                'description': seg.segment_descript or '',
                })

    return JsonResponse({
        'res': 'ok', 'data': {
            'media_path': media_path,
            'details': '',
            'key_words': [],
            'subtitle_list': subtitle_list,
            'head_list': head_list,
            'key_frame_list': key_frame_list,
            'segment_list': segment_list,
            'first_segment_poster': first_segment_poster,
            'thumb_list': thumb_list,
            'program_name': program.program_name,
            'series_name': program.series_name
        }})


# 根据分段第一帧获取该分段视频信息
def get_segment_info(request):

    segment_frame = request.GET.get('segment_frame')
    series_name = request.GET.get('series_name')
    program_name = request.GET.get('program_name')

    segment_set = Segment.objects.filter(segment_start_num=segment_frame, program_name=program_name, series_name=series_name)
    if not segment_set:
        return JsonResponse({'res': 'error', 'msg': 'no segment!'})

    segment = segment_set[0]
    # program_set = Program.objects.filter(program_name=segment.program_name)
    # if not program_set:
    #     return JsonResponse({'res': 'error', 'msg': 'no program!'})

    # program = program_set[0]
    # subtitle_list = eval(program.frame_text or '[]')

    # segment_subtitle_list = []
    # for sub in subtitle_list:
    #     if sub.get('frame') <= segment.segment_end_num and sub.get('frame') >= segment.segment_start_num:
    #         segment_subtitle_list.append(sub)

    return JsonResponse({
        'res': 'ok',
        'data': {
            'segment_start_time': segment.segment_start_num,
            'segment_end_time': segment.segment_end_num,
            'segment_keywords': eval(segment.segmengt_keywords or '[]'),
            'segment_description': segment.segment_descript,
            # 'segment_subtitle_list': segment_subtitle_list,

        }
    })


def edit_segment_description(request):

    segment_frame = request.GET.get('segment_frame')
    series_name = request.GET.get('series_name')
    program_name = request.GET.get('program_name')
    description = request.GET.get('description')

    segment_set = Segment.objects.filter(segment_start_num=segment_frame, program_name=program_name, series_name=series_name)
    if not segment_set:
        return JsonResponse({'res': 'error', 'msg': 'no segment!'})

    try:
        segment = segment_set[0]
        segment.segment_descript = description
        segment.save()

        return JsonResponse({'res': 'ok', 'msg': 'success!'})
    except:
        return JsonResponse({'res': 'error', 'msg': 'save fail!'})


def edit_program_subtitle(request):

    segment_frame = request.GET.get('segment_frame')
    program_name = request.GET.get('program_name')
    series_name = request.GET.get('series_name')
    subtitle = request.GET.get('subtitle')

    program_set = Program.objects.filter(program_name=program_name, series_name=series_name)
    if not program_set:
        return JsonResponse({'res': 'error', 'msg': 'no program!'})

    try:
        modify_subtitle_list = []
        program = program_set[0]
        subtitle_list = eval(program.frame_text or '[]')
        for sub in subtitle_list:
            if sub.get('frame_num') == int(segment_frame):
                modify_subtitle_list.append({'frame_num': sub.get('frame_num'), 'text': subtitle})
            else:
                modify_subtitle_list.append(sub)
        program.frame_text = modify_subtitle_list
        program.save()

        return JsonResponse({'res': 'ok', 'msg': 'success!'})
    except:
        return JsonResponse({'res': 'error', 'msg': 'save fail!'})


def edit_series_info(request):

    series_name = request.GET.get('series_name')
    field_type = request.GET.get('field_type')
    field_value = request.GET.get('field_value')

    series_set = Series.objects.filter(series_name=series_name)
    if not series_set:
        return JsonResponse({'res': 'error', 'msg': 'no series!'})

    try:
        series = series_set[0]
        setattr(series, field_type, field_value)
        series.save()
        return JsonResponse({'res': 'ok', 'msg': 'success'})
    except:
        import traceback
        print(traceback.format_exc())
        return JsonResponse({'res': 'error', 'msg': 'save fail!'})


def get_page_program(request):

    series_name = request.GET.get('series_name')
    page_index = int(request.GET.get('page_index', 1))
    program_set = Program.objects.filter(series_name=series_name)
    program_page_set = program_set[(page_index-1)*22: page_index*22]

    program_list = []
    if program_page_set:
        program_list = [{'program_name': p.program_name, 'series_name': p.series_name} for p in program_page_set]

    else:
        return JsonResponse({'res': 'error', 'msg': '已经最后一页了！'})

    return JsonResponse({
        'res': 'ok', 'data': {
            'program_list': program_list,
        }})


def main(request):
    news_series_set = Series.objects.filter(series_type='新闻')

    news_series_list = [{
        'series_name': news.series_name, 
        'surface_image': news.surface_image, 
        'series_type': news.series_type,
        'program_list': [p.program_name for p in Program.objects.filter(series_name=news.series_name)[: 7]],
    } for news in news_series_set]

    return render(request, 'main.html', {'news_series_list': news_series_list, })


def get_series_by_type(request):

    series_type = request.GET.get('series_type')
    series_set = Series.objects.filter(series_type=series_type)

    series_list = [{
        'series_name': series.series_name, 
        'surface_image': series.surface_image, 
        'series_type': series.series_type,
        'program_list': [p.program_name for p in Program.objects.filter(series_name=series.series_name)[: 7]],
    } for series in series_set]

    return JsonResponse({
        'res': 'ok',
        'data': series_list
        })


def main_search(request):

    series_name = request.GET.get('series_name')

    series_set = Series.objects.filter(series_name__icontains=series_name)
    series_list = [{
        'series_name': series.series_name, 
        'surface_image': series.surface_image, 
        'series_type': series.series_type,
        'program_list': [p.program_name for p in Program.objects.filter(series_name=series.series_name)[: 7]],
    } for series in series_set]

    return JsonResponse({
        'res': 'ok',
        'data': series_list
        })


def profile_index(request):
    return render(request, 'upload.html', {})


def upload_files(request):

    try:
        series_type = request.POST.get('series_type') or ''
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tmp_dir = os.path.join(base_dir, 'static')
        folder_name = request.POST.get('folder_name') or '未命名'
        tmp_folder = os.path.join(tmp_dir, folder_name)
        dist_folder = os.path.join(base_dir, 'process', 'media', folder_name)
        if os.path.exists(tmp_folder):
            os.remove(tmp_folder)
        if os.path.exists(dist_folder):
            os.remove(dist_folder)
        os.mkdir(tmp_folder)

        all_files = request.FILES.getlist('series_dir')
        for single_file in all_files:
            file_dir = os.path.join(tmp_folder, single_file.name)
            with open(file_dir, 'wb') as f:
                pieces = single_file.chunks(chunk_size=10000000)
                for piece in pieces:
                    f.write(piece)
                f.close()

        shutil.move(tmp_folder, dist_folder)
        surface_image = '/static/media/'+folder_name+'/surface.jpg'
        print(surface_image)
        series_obj = Series(series_name=folder_name, series_type=series_type,surface_image=surface_image)
        series_obj.save()

    except:
        import traceback
        print(traceback.format_exc())
        return JsonResponse({'res': 'error', 'msg': traceback.format_exc()})

    return render(request, 'upload.html', {})


