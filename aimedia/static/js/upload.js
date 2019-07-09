$(function(){

	$("#upload_input_ctl").click(function(){
		$("#upload_input").click();
	})

	$("#upload_input").on('change', function(e){
		var all_files = e.target.files;
	    var relative_path = all_files[0].webkitRelativePath;
	    var folder_set = relative_path.split("/");
	    var folder_name = folder_set[0];

	    if (folder_name) $("#folder_name_box").val(folder_name);

	    var item_dom_str = '';
	    $(".upload-detail-box").html('');
	    for(var i=0; i<all_files.length; i++){
	    	item_dom_str += '<div class="upload-item-detail">' + all_files[i].name + '</div> ' 
	    }
	    $(".upload-detail-box").html(item_dom_str);
	    $("#upload_files_form").submit();
	})
})