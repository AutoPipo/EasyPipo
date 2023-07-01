function close_btn(target){
    $(".fileBox").remove();
    $("#file").val(null);
    $(".go_btn").hide();
}





$(window).on('load', function(){

    let ori_image_path = null;
    let ren_image_path = null;
    sessionStorage.setItem("reduce_data", -1)

    $('.zone').on("dragover", dragOver).on("drop", uploadFiles);
                
    $("#file").change(function(e){
        uploadFiles(e);
    });

    function dragOver(e) {
        if($(e.target).get(0) != $('#file').get(0)){
            e.stopPropagation();
            e.preventDefault();
        }

        let dropZone = $('.zone'),
            timeout = window.dropZoneTimeout;
        if (!timeout) {
            dropZone.addClass('in');
        }
        else {
            clearTimeout(timeout);
        }
        let found = false,
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
        let files = e.target.files || e.dataTransfer.files;

        selectFile(files, e);
    }


    function do_image_job(job, next_btn, image_path){
        $('.loader').addClass('is-active');

        if(job == "reduceColor"){
            reduce_data = ""
            $('.cluster_number_input').each(function(){
                reduce_data += $(this).val()+",";
            });
            reduce_data += $("#mycolor_check").is(":checked");
            sessionStorage.setItem("reduce_data", reduce_data)
        }
        else if(job == "drawLine"){
            image_path = $("input[name='reduce_img_select']:checked + > img").attr("src");
            reduce_data = $("input[name='reduce_img_select']:checked").val();
            sessionStorage.setItem("reduce_data", reduce_data)
        }
        else{
            reduce_data = sessionStorage.getItem("reduce_data")
        }

        $.ajax({
            url: `/imageProcess/${job}`,
            data: {
                "image_path": image_path,
                "reduce_data": sessionStorage.getItem("reduce_data")
            },
            dataType:'json',
            type: 'POST',
            success: function (data) {
                $(data.target+'_box').show();
                $(data.target+'_box').parent().addClass('is-done');
                $($(data.target+'_box').parent()).removeClass('current');
                $($(data.target+'_box').parent().next()).addClass('current');

                let time = new Date().getTime();

                if(job == "reduceColor") {
                    let img_name = data.img_name.split(".")[0]
                    let split_img_name = data.img_name.split(".")[1]
                    
                    $(".color_text").each(function(idx){
                        let cluster = data.clusters[idx]

                        $(`${data.target}_${idx+1} img`).attr(
                            'src',
                            `/static/render_image/${img_name}_${cluster}.${split_img_name}?time=${time}`
                        )

                        $(`${data.target}_${idx+1}`).css(
                            'background-image',
                            `url(/static/render_image/${img_name}_${cluster}.${split_img_name}?time=${time}`
                        )

                        $(this).text(`${cluster} Color`);
                        
                        $(".download_btn").eq(idx+1).attr("href", `/static/render_image/${img_name}_${cluster}.${split_img_name}`)
                        $(`#a_reduce_input_${idx+1}`).attr("href", `/static/render_image/${img_name}_${cluster}.${split_img_name}?time=${time}`)
                    })
                }
                else{
                    $(data.target).attr('src', `/static/render_image/${data.img_name}?time=${time}`);
                }

                $(next_btn).show();

                $('.loader').removeClass('is-active');

                $('html,body').animate({ scrollBottom: 300 }, 'slow'); // 9999
            },
            error: function (error) {
                console.error(error);
            }
        });
    }
    
    
    function selectFile(fileObject, e){
        let files = null;

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
                $(".go_btn").show();
                $(".view_image_box").hide();
                $(".btn_box").hide();



                $(".zone").css({"outline": "none"});

                $('.view_image_box,.view_image_box').hide();

                let tag = '';
                let f = files[0];
                let fileName = f.name;
                let fileSize = f.size / 1024 / 1024;
                fileSize = fileSize < 1 ? fileSize.toFixed(3) : fileSize.toFixed(1);

                tag += 
                    "<div class='fileBox'>" +
                        "<image id='thumbnail'>" +
                        "<span class='x_btn' onclick='close_btn(this);'>x</span>" +
                        "<div class='filename_text'>"+fileName+"<br>"+fileSize+" MB</div>" +
                    "</div>";

                $("#non-upload-box").css("display", "none");
                $("#dropZ").append(tag);

                $('html,body').animate({ scrollTop: 9999 }, 'slow');

                let reader = new FileReader();
                reader.onload = function(e){
                    $("#thumbnail").attr("src", e.target.result);
                }
                reader.readAsDataURL(f);

                // GO 버튼 클릭 (첫 시작)
                $('.go_btn').click(function(){
                    let formData = new FormData();
                    formData.append("file", f);

                    sessionStorage.setItem("org_image_path", `../static/org_image/${fileName}`)
                    sessionStorage.setItem("ren_image_path", `../static/render_image/${fileName}`)

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
                            org_image_path = sessionStorage.getItem("org_image_path")
                            do_image_job("processStart", "#reduce_btn", org_image_path);
                            $("#reduce_box").show();
                            $(".download_btn").eq(0).attr("href", org_image_path);
                        },
                        error: function (error) {
                            console.error(error);
                        }
                    });
                });

                // Reduce Color 버튼 클릭 (2번째)
                $("#reduce_btn").click(function(){
                    ren_image_path = sessionStorage.getItem("ren_image_path")

                    do_image_job("reduceColor", "#drawline_btn", ren_image_path);
                    
                    baguetteBox.run('.reduce_img_baguette', {
                        noScrollbars: true
                    });
                })

                $("#drawline_btn").click(function(){
                    ren_image_path = sessionStorage.getItem("ren_image_path")
                    do_image_job("drawLine", "#numbering_btn", ren_image_path)

                    let temp = ren_image_path.split(".")
                    $(".download_btn").eq(4).attr("href", ren_image_path)
                    $(".download_btn").eq(4).attr("href", `..${temp[2]}_linedraw.${temp[3]}`)
                })

                $("#numbering_btn").click(function(){
                    ren_image_path = sessionStorage.getItem("ren_image_path")
                    do_image_job("numbering", null, ren_image_path)
                    
                    let temp = ren_image_path.split(".")
                    $(".download_btn").eq(5).attr("href", `..${temp[2]}_numbering.${temp[3]}`)

                    $("#input_color_label_btn").show();

                    $("#input_color_label_btn").click(
                        function(){
                            let time = new Date().getTime();

                            let state = $(this).data('toggleState');

                            if(state){
                                $("#numbering_img").attr('src', `..${temp[2]}_numbering_label.${temp[3]}'?time=${time}`)
                                $(".download_btn").eq(5).attr("href", `..${temp[2]}_numbering_label.${temp[3]}`)
                            }
                            else{
                                $("#numbering_img").attr('src', `..${temp[2]}_numbering.${temp[3]}'?time=${time}`)
                                $(".download_btn").eq(5).attr("href", `..${temp[2]}_numbering.${temp[3]}`)
                            }
                            $(this).data('toggleState', !state);
                        }
                    );
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