function close_btn(target){
    // alert(target);
    $(".fileBox").remove();
    $("#file").val(null);
}

$(window).on('load', function(){
    var ori_image_path = null;
    var ren_image_path = null;

    $('.zone').on("dragover", dragOver).on("drop", uploadFiles);
                
    $("#file").change(function(e){
        uploadFiles(e);
    });

    function dragOver(e) {
        if($(e.target).get(0) != $('#file').get(0)){
            e.stopPropagation();
            e.preventDefault();
        }

        var dropZone = $('.zone'),
            timeout = window.dropZoneTimeout;
        if (!timeout) {
            dropZone.addClass('in');
        }
        else {
            clearTimeout(timeout);
        }
        var found = false,
            node = e.target;

        do {
            if (node === dropZone[0]) {
                found = true;
                break;
            }
            node = node.parentNode;
        } while (node != null);

        if (found) {
            dropZone.addClass('hover');
        }
        else {
            dropZone.removeClass('hover');
        }
        window.dropZoneTimeout = setTimeout(function () {
            window.dropZoneTimeout = null;
            dropZone.removeClass('in hover');
        }, 100);
    }

    function uploadFiles(e) {
        if($(e.target).get(0) != $('#file').get(0)){
            e.stopPropagation();
            e.preventDefault();
            dragOver(e);
        }
        
        e.dataTransfer = e.originalEvent.dataTransfer;
        var files = e.target.files || e.dataTransfer.files;

        selectFile(files, e);
    }


    function do_image_job(job, next_btn, image_path){
        $('.loader').addClass('is-active');
        var reduce_data = "";

        if(job == "reduce_color"){
            $('.cluster_number_input').each(function(){
                reduce_data += $(this).val()+",";
            });
            reduce_data += $("#mycolor_check").is(":checked");
        }
        else if(job == "draw_line"){
            reduce_data = $("input[name='reduce_img_select']:checked").val();
            
        }
        else{
            reduce_data = -1;
        }

        $.ajax({
            url: '/convert',
            data: {"job":job, "image_path": image_path, "reduce_data":reduce_data},
            dataType:'json',
            type: 'POST',
            success: function (data) {
                $(data.target+'_box').show();

                var time = new Date().getTime();

                if(job == "reduce_color"){
                    var img_name = data.img_name.split(".")[0];
                    $(data.target+"_1"+" img").attr('src', '/static/render_image/'+img_name+'_1.png?time='+time);
                    $(data.target+"_2"+" img").attr('src', '/static/render_image/'+img_name+'_2.png?time='+time);
                    $(data.target+"_3"+" img").attr('src', '/static/render_image/'+img_name+'_3.png?time='+time);
                    
                    $(data.target+"_1").css('background-image', 'url(/static/render_image/'+img_name+'_1.png?time='+time+')');
                    $(data.target+"_2").css('background-image', 'url(/static/render_image/'+img_name+'_2.png?time='+time+')');
                    $(data.target+"_3").css('background-image', 'url(/static/render_image/'+img_name+'_3.png?time='+time+')');
                }
                else{
                    $(data.target).attr('src', '/static/render_image/'+data.img_name+'?time='+time);
                }

                $(next_btn).show();

                $('.loader').removeClass('is-active');

                $('html,body').animate({ scrollTop: 9999 }, 'slow');
            },
            error: function (error) {
                console.error(error);
            }
        });
    }
    
    
    function selectFile(fileObject, e){
        var files = null;

        if(fileObject == undefined){

        }

        if(fileObject != null){
            files = fileObject;
        }
        else{
            files = $("#file").files;
        }

        if(files != null && files[0] != undefined){
            if (files.length > 1 || $("#dropZ .fileBox").length>0 ){
                alert('파일은 1개만 업로드할 수 있습니다.');
                return;
            }

            if (files[0].type==='image/jpeg' || files[0].type==='image/png') {
                $(".zone").css({"outline": "none"});

                $('.view_image_box,.view_image_box').hide();

                var tag = '';
                var f = files[0];
                var fileName = f.name;
                var fileSize = f.size / 1024 / 1024;
                fileSize = fileSize < 1 ? fileSize.toFixed(3) : fileSize.toFixed(1);

                // "<image src=\'{{url_for('static',filename='css/icon/preview_image.png')}}\'>" +
                tag += 
                    "<div class='fileBox'>" +
                        "<image id='thumbnail'>" +
                        "<span class='x_btn' onclick='close_btn(this);'>x</span>" +
                        "<div class='filename_text'>"+fileName+"<br>"+fileSize+" MB</div>" +
                    "</div>";

                $("#non-upload-box").css("display", "none");
                $("#dropZ").append(tag);

                $('html,body').animate({ scrollTop: 9999 }, 'slow');

                var reader = new FileReader();
                reader.onload = function(e){
                    $("#thumbnail").attr("src", e.target.result);
                }
                reader.readAsDataURL(f);

                $('.go_btn').click(function(){
                    var formData = new FormData();
                    formData.append("file", f);
                    ori_image_path = '../static/org_image/'+fileName;
                    ren_image_path = '../static/render_image/'+fileName;

                    $.ajax({
                        type: 'POST',
                        url: '/uploadIMG',
                        processData: false,
                        contentType: false,
                        xhrFields: {
                            withCredentials: true
                        },
                        data: formData,
                        success: function (data) {
                            do_image_job("start", "#reduce_btn", ori_image_path);
                            $("#reduce_box").show();
                        },
                        error: function (error) {
                            console.error(error);
                        }
                    });
                });

                $("#reduce_btn").click(function(){
                    do_image_job("reduce_color", "#drawline_btn", ren_image_path);
                })

                $("#drawline_btn").click(function(){
                    do_image_job("draw_line", "#numbering_btn", ren_image_path);
                })

                $("#numbering_btn").click(function(){
                    do_image_job("numbering", null, ren_image_path);
                    // $("#numbering_btn").show();
                })
            }
            else{
                alert('이미지 파일만 업로드할 수 있습니다.');
                $("#file").val(null);
                return;
            }
        }
    }
});




function distanceBetween(point1, point2) {
    return Math.sqrt(Math.pow(point2.x - point1.x, 2) + Math.pow(point2.y - point1.y, 2));
}
function angleBetween(point1, point2) {
    return Math.atan2( point2.x - point1.x, point2.y - point1.y );
}