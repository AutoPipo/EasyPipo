$(window).on('load', function(){
    var image_path = '../static/org_image/222.jpg';
    var pic_size = 600;

    var brush_cursor = document.querySelector('.brush_cursor');
    var brush_size = 20;
    var area_arr = [];
    var img_size_origin = {};
    var img_size = {};

    
    var pic_canvas = document.getElementById('canvas_pic');
    var result_canvas = document.getElementById('canvas_result');

    var ctx = '';
    var result_ctx = '';
    
    make_base(image_path);


    // diy makers Javascript
    function clearit() {
        // ctx.clearRect(0,0, 1000, 1000);
        make_base(image_path);
        brush_size = 20;
		
    }

    // 슬라이드 조절 시 브러시 사이즈 변경
    $('#brush_size').change(function(e){
        brush_size = $(this).val();
        
        $(brush_cursor).css('width', brush_size*2);
        $(brush_cursor).css('height', brush_size*2);
    });

    $('.convert_box p').click(function(){
        $('.loader').addClass('is-active');

        var working = setInterval(function(){
            image = new Image();
            var time = new Date().getTime();
            image.src = '../static/render_image/working_img.png?time='+time;
            var width_set = pic_size;
            var height_set = pic_size * image.height / image.width;
    
            result_ctx.drawImage( image, 0, 0, width_set, height_set );

        }, 3000);

        

        $.ajax({
            url: '/convert',
            data: {
                "image_path":image_path,
                "area_arr":JSON.stringify(area_arr),
                "line_detail":$("#line_detail").val(),
				"blur_size":$("#blur_size").val() // koo
            },
            dataType:'json',
            type: 'POST',
            success: function (data) {
                clearInterval(working);

                image = new Image();
                var time = new Date().getTime();

                image.src = '/static/render_image/'+data.img_name+'?time='+time;
                
                $(image).on('load', function(){
                    var width_set = pic_size;
                    var height_set = pic_size * image.height / image.width;

                    result_ctx.drawImage( image, 0, 0, width_set, height_set );

                    $("#result_img_url").text(data.img_name);
                    $('#result_download_btn').css('visibility', 'visible');

                    $('.loader').removeClass('is-active');
                });
				
				area_arr = []; // koo
            },
            error: function (error) {
                console.error(error);
            }
        });

        clearit();
    });


    // 캔버스 기본 세팅
    function make_base(path) {
        image = new Image();
        image.src = path;

        $(image).on('load', function(){
            var width_set = pic_size;
            var height_set = pic_size * image.height / image.width;

            pic_canvas.width = width_set;
            pic_canvas.height = height_set;

            pic_canvas.style.width = width_set;
            pic_canvas.style.height = height_set;

            result_canvas.width = width_set;
            result_canvas.height = height_set;

            img_size = {width:width_set, height:height_set};
            img_size_origin = {width:image.width, height:image.height};


            ctx = pic_canvas.getContext('2d');
            result_ctx = result_canvas.getContext('2d');

            ctx.fillStyle = "rgba(255, 0, 0, 0.05)";
            
            // ctx.globalAlpha = "0.5";
            ctx.lineWidth = 0;
            ctx.globalCompositeOperation = "source-over"; 

            
            //drawImage(이미지객체, 
            //  이미지의 왼위 부분x, 이미지의 왼위 부분y, 이미지의 원하는 가로크기, 
            //  이미지의 원하는 세로크기,
            //  사각형 부분x, 사각형 부분y, 가로크기, 세로크기)
            ctx.drawImage( image, 0, 0, width_set, height_set );

            $("#target_img_url").text(path);
            $(".canvas_box, .convert_box").css('height', height_set + 90);

            
            var isDrawing, lastPoint;

            
            pic_canvas.onmousedown = function(e) {
                isDrawing = true;
                lastPoint = { x: e.offsetX, y: e.offsetY }; // 왼쪽 위
            };

            pic_canvas.onmousemove = function(e) {
                var x = e.clientX;
                var y = e.clientY;
                brush_cursor.style.left = x + "px";
                brush_cursor.style.top = y + "px";


                if (!isDrawing){
                    return;
                }
                
                var currentPoint = { x: e.offsetX, y: e.offsetY }; // 왼쪽 위

                var dist = distanceBetween(lastPoint, currentPoint);
                var angle = angleBetween(lastPoint, currentPoint);
                
                var x_value = 0; // x좌표
                var y_value = 0; // y좌표

                for (i = 0; i < dist; i += 3) {
                    x = lastPoint.x + (Math.sin(angle) * i);
                    y = lastPoint.y + (Math.cos(angle) * i);

                    ctx.beginPath();
                    // x좌표, y좌표, 반지름
                    ctx.arc(x + x_value, y + y_value, brush_size, false, Math.PI * 2, false);
                    ctx.closePath();
                    ctx.fill();


                    scalingFactorX = img_size_origin['width'] / img_size['width'];
                    scalingFactorY = img_size_origin['height'] / img_size['height'];
                    
                    x1 = (x + x_value) * scalingFactorX;
                    y1 = (y + y_value) * scalingFactorY;

                    area_arr.push({x:x1, y:y1, radius:brush_size * scalingFactorX});
                }
                
                lastPoint = currentPoint;
            };
            
            pic_canvas.onmouseup = function() {
                isDrawing = false;
            };


            
            $("#pic_clear_btn").click(function(){
                clearit();
            });
        });

        
    }
});




function distanceBetween(point1, point2) {
    return Math.sqrt(Math.pow(point2.x - point1.x, 2) + Math.pow(point2.y - point1.y, 2));
}
function angleBetween(point1, point2) {
    return Math.atan2( point2.x - point1.x, point2.y - point1.y );
}