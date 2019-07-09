$(function(){
	$(".program-type-item").click(function(){
		$(".program-type-item").removeClass('program-type-item-active');
		$(this).addClass('program-type-item-active');
		$.get('/media/get_series_by_type/?series_type=' + $(this).html(), function(result){
			if (result.res == 'ok'){
				var combine_dom_str = '';
				$('.series-view').html('');
				for(var i=0; i<result.data.length; i++){
					combine_dom_str += '<div class="item-box" series_name="' + result.data[i].series_name + '"> <div class="item-image"> <img src="' + result.data[i].surface_image + 
					'"> </div>  <div class="item-name">' + result.data[i].series_name + '</div>';
					for(var j=0; j<result.data[i].program_list.length; j++){
						combine_dom_str += '<div class="item-index">' + result.data[i].program_list[j] + '</div> ';
					}
					combine_dom_str += '</div>';
				}
				$('.series-view').html(combine_dom_str);
			}
			else alert(result.msg);
		})
	})

	$(".series-view").on('click', 'img', function(){
		var series_name = $(this).parent().parent().attr('series_name');
		location.href = '/media/?series_name=' + series_name;
	})

	$('.search-bar > input').bind('keypress',function(event){
        if(event.keyCode == 13)      
        {  
        	$.get('/media/main_search/?series_name=' + $(this).val(), function(result){
        		if (result.res == 'ok'){
					var combine_dom_str = '';
					$('.series-view').html('');
					for(var i=0; i<result.data.length; i++){
						combine_dom_str += '<div class="item-box" series_name="' + result.data[i].series_name + '"> <div class="item-image"> <img src="' + result.data[i].surface_image + 
						'"> </div>  <div class="item-name">' + result.data[i].series_name + '</div>';
						for(var j=0; j<result.data[i].program_list.length; j++){
							combine_dom_str += '<div class="item-index">' + result.data[i].program_list[j] + '</div> ';
						}
						combine_dom_str += '</div>';
					}
					$('.series-view').html(combine_dom_str);
				}
				else alert(result.msg);
        	})
        }  
    });


    $(".series-view").on('click', '.item-index', function(){
    	var program_name = $(this).html();
    	var series_name = $(this).parent().attr('series_name');

    	location.href = '/media/?series_name=' + series_name + '&program_name=' + program_name;
    })
})
