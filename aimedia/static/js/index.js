videojs.options.flash.swf = "video-js.swf";

var myPlayer = videojs('main_video', {
    "controls": true,
    "autoplay": true,
    // "techOrder" : [ "html5", "flash" ]
});
var main_view_height = $(".main_view").height();
var main_view_width = $(".main_view").width();
myPlayer.width(main_view_width);
myPlayer.height(main_view_height);

myPlayer.load();


function wait_to_pause(segment_end_time){
    var time = myPlayer.currentTime() + ""; 
    var ts = time.substring(0, time.indexOf(".")); 
    if(parseInt(ts) == segment_end_time){
        myPlayer.pause(); 
    }
}

var pause_interval_id = null;

$(function () {
    
    $("#segment_view_ctl").click(function () {
        $(".view_group").hide();
        $(".thumbnail_view").show();
    });

    $("#subtitles_view_ctl").click(function () {
        $(".view_group").hide();
        $(".subtitles_view").show();
    });

    $("#heads_view_ctl").click(function () {
        $(".view_group").hide();
        $(".heads_view").show();
    });

    $("#key_frames_view_ctl").click(function () {
        $(".view_group").hide();
        $(".key_frames_view").show();
    });

    $("#details_view_ctl").click(function () {
        $(".view_group").hide();
        $(".details_view").show();
    });

    $(".main_tab_btn").click(function () {
        $(".main_tab_btn").removeClass('main_tab_btn_active');
        $(this).addClass('main_tab_btn_active');
    });


    $(".program_item").click(function () {

        var program_name = $(this).html();
        var series_name = $(this).attr('series_name')
        $.get('/media/get_program_info/?program_name=' + program_name + '&series_name=' + series_name, function (rsp) {
            var result = rsp;
            if(result.res != 'ok') alert(result.msg);
            else{

                $(".thumbnail_view").html('');
                var segment_list = result.data.segment_list;
                var segment_dom_str = '<div style="height:450px; margin-top: 10px;"> <div style="overflow-y:scroll;height: 524px;">';
                for(var i=0; i<segment_list.length; i++){
                    segment_dom_str += '<div class="segment_items" frame_id="' + result.data.thumb_list[i].frame_id + '" program_name="' + 
                    result.data.program_name + '" series_name="' + result.data.series_name + '"> <img class="segment_thumbnail" src="' +
                        result.data.thumb_list[i].thumb + '"> <input class="segment_description" value="' + result.data.thumb_list[i].description + 
                        '" readonly="true"> </div>';
                }
                segment_dom_str += '</div> </div>';
                $(".thumbnail_view").html(segment_dom_str);

                //$(".page_index").eq(0).html(1);

                $(".subtitle_text_box").html('');
                var subtitle_list = result.data.subtitle_list;
                var subtitle_dom_str = '';
                for(var i=0; i<subtitle_list.length; i++){
                    subtitle_dom_str += '<div class="subtitle_items" frame_id="' + subtitle_list[i].frame_num + 
                    '" program_name="' + program_name + '" series_name="' + series_name + '"> <input class="subtitle_items_text" value="' + 
                    subtitle_list[i].text + '" readonly="true"> </div>';
                }
                $(".subtitle_text_box").html(subtitle_dom_str);

                $(".head_items_box").html('');
                var head_list = result.data.head_list;
                var head_dom_str = ''
                for(var i=0; i<head_list.length; i++){
                    head_dom_str += '<div class="head_items"> <img class="head_thumbnail" src="' +
                        result.data.head_list[i] + '"> </div>';
                }
                $(".head_items_box").html(head_dom_str);

                $(".key_frame_box").html('');
                var key_frame_list = result.data.key_frame_list;
                var key_frame_dom_str = ''
                for(var i=0; i<key_frame_list.length; i++){
                    key_frame_dom_str += '<div class="key_frame_items"> <img class="key_frame_thumbnail" src="' +
                        result.data.key_frame_list[i] + '"> </div>';
                }
                $(".key_frame_box").html(key_frame_dom_str);

                myPlayer.src(result.data.media_path);
                myPlayer.poster(result.data.first_segment_poster);
                myPlayer.load();
            }
        })
    })


    $(".thumbnail_view").on('click', '.segment_items', function(){
        var frame_id = $(this).attr('frame_id');
        var program_name = $(this).attr('program_name');
        var series_name = $(this).attr('series_name');
  
        $.get('/media/get_segment_info/?segment_frame=' + frame_id + '&program_name=' + program_name + '&series_name=' + series_name, function(result){
            if(result.res == 'ok'){
                myPlayer.pause();
                if(pause_interval_id) window.clearInterval(pause_interval_id);
                var segment_start_time = result.data.segment_start_time;
                var segment_end_time = result.data.segment_end_time;
                myPlayer.currentTime(segment_start_time);
                var interval_id = window.setInterval("wait_to_pause(" + segment_end_time + ")", 1000);
                pause_interval_id = interval_id;
            
            }
        })
    })

    // $(".thumbnail_view").on('click', 'button', function(){
    //     var description = $(this).parent().find('input').val();
    //     var segment_frame = $(this).parent().attr('frame_id');
    //     var program_name = $(this).parent().attr('program_name');
    //     var series_name = $(this).parent().attr('series_name');
    //     $.get('/media/edit_segment_description/?program_name=' + program_name + '&segment_frame=' + segment_frame + '&description=' + description + '&series_name=' + series_name, 
    //         function(result){
    //         if(result.res == 'ok') alert('修改成功！');
    //         else alert('修改失败！');
    //     })
    //     $(this).parent().find('input').attr('readonly', 'true');
    // })

    $(".thumbnail_view").on('dblclick', 'input', function(){
        $(this).removeAttr('readonly');
        $(this).focus();
    })

    $('.thumbnail_view').on('keypress', 'input', function(event){
        if(event.keyCode == 13)      
        {  
            var description = $(this).parent().find('input').val();
            var segment_frame = $(this).parent().attr('frame_id');
            var program_name = $(this).parent().attr('program_name');
            var series_name = $(this).parent().attr('series_name');
            var this_input = $(this);
            $.get('/media/edit_segment_description/?program_name=' + program_name + '&segment_frame=' + segment_frame + '&description=' + description + '&series_name=' + series_name, 
                function(result){
                if(result.res == 'ok'){
                    this_input.parent().next().find('input').dblclick();
                }
                else{
                    alert('修改失败！');
                    this_input.dblclick();
                };
            })
            $(this).attr('readonly', 'true');
        }  
    });

    $(".prev_page").click(function(){
        var page_index = parseInt($(".page_index").eq(0).html());
        var series_name = $(".program_view").find('div').eq(0).attr('series_name');

        if(page_index <= 1) return;

        page_index -= 1;

        $.get('/media/get_page_program/?&page_index=' + page_index + '&series_name=' + series_name, function(result){
            if(result.res != 'ok') alert(result.msg);
            else{
                $(".program_view").html('');
                var program_dom_str = '';
                for(var i=0; i<result.data.program_list.length; i++){
                    program_dom_str += '<div class="program_item" series_name="' + result.data.program_list[i].series_name + 
                    '">' + result.data.program_list[i].program_name + '</div>'
                }
                $(".program_view").html(program_dom_str);
                $(".page_index").eq(0).html(page_index);
            }
        })
    })

    $(".next_page").click(function(){
        var page_index = parseInt($(".page_index").eq(0).html());
        var series_name = $(".program_view").find('div').eq(0).attr('series_name');

        page_index += 1;

        $.get('/media/get_page_program/?&page_index=' + page_index + '&series_name=' + series_name, function(result){
            if(result.res != 'ok') alert(result.msg);
            else{
                $(".program_view").html('');
                var program_dom_str = '';
                for(var i=0; i<result.data.program_list.length; i++){
                    program_dom_str += '<div class="program_item" series_name="' + result.data.program_list[i].series_name + 
                    '">' + result.data.program_list[i].program_name + '</div>'
                }
                $(".program_view").html(program_dom_str);
                $(".page_index").eq(0).html(page_index);
            }
        })
    })


    $(".subtitle_text_box").on('click', 'div', function(){
        var frame_id = $(this).attr('frame_id');
        var program_name = $(this).attr('program_name');
        var series_name = $(this).attr('series_name');
  
        $.get('/media/get_segment_info/?segment_frame=' + frame_id + '&program_name=' + program_name + '&series_name=' + series_name, function(result){
            if(result.res == 'ok'){
                myPlayer.pause();
                if(pause_interval_id) window.clearInterval(pause_interval_id);
                var segment_start_time = result.data.segment_start_time;
                var segment_end_time = result.data.segment_end_time;
                myPlayer.currentTime(segment_start_time);
                var interval_id = window.setInterval("wait_to_pause(" + segment_end_time + ")", 1000);
                pause_interval_id = interval_id;
            
            }
        })
    })

    // $(".subtitle_text_box").on('click', 'button', function(){
    //     var subtitle = $(this).parent().find('input').val();
    //     var segment_frame = $(this).parent().attr('frame_id');
    //     var program_name = $(this).parent().attr('program_name');
    //     var series_name = $(this).parent().attr('series_name');
    //     $.get('/media/edit_program_subtitle/?program_name=' + program_name + '&segment_frame=' + segment_frame + '&subtitle=' + subtitle + '&series_name=' + series_name, 
    //         function(result){
    //         if(result.res == 'ok') alert('修改成功！');
    //         else alert('修改失败！');
    //     })
    //     $(this).parent().find('input').attr('readonly', 'true');
    // })

    $(".subtitle_text_box").on('dblclick', 'input', function(){
        $(this).removeAttr('readonly');
        $(this).focus();
    })

    $('.subtitle_text_box').on('keypress', 'input', function(event){
        if(event.keyCode == 13)      
        {  
            var subtitle = $(this).parent().find('input').val();
            var segment_frame = $(this).parent().attr('frame_id');
            var program_name = $(this).parent().attr('program_name');
            var series_name = $(this).parent().attr('series_name');
            var this_input = $(this);
            $.get('/media/edit_program_subtitle/?program_name=' + program_name + '&segment_frame=' + segment_frame + '&subtitle=' + subtitle + '&series_name=' + series_name, 
                function(result){
                if(result.res == 'ok'){
                    this_input.parent().next().find('input').dblclick();
                }
                else{
                    alert('修改失败！');
                    this_input.dblclick();
                };
            })
            $(this).attr('readonly', 'true');
        }  
    });


    $(".detail_box").on('keypress', 'input', function(event){
        if(event.keyCode == 13)      
        {  
            var field_type = $(this).attr('field_type');
            var series_name = $(this).attr('series_name');
            var this_input = $(this);
            $.get('/media/edit_series_info/?series_name=' + series_name + '&field_type=' + field_type + '&field_value=' + $(this).val(), 
                function(result){
                if(result.res == 'ok'){
                    this_input.parent().next().find('input').focus();
                }
                else{
                    alert('修改失败！');
                    this_input.focus()
                };
            })
            $(this).attr('readonly', 'true');
        }  
    });


    if ($("#hidden_click_program_name").val()){
        var all_current_programs = $(".program_item");
        for(var i=0; i<all_current_programs.length; i++){
            if(all_current_programs.eq(i).html() == $("#hidden_click_program_name").val()){
                all_current_programs.eq(i).click();
                break;
            }
        }
    }



})







