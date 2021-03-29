$(window).on('load', function(){
    var image_path = '../static/test-image/aa.jpg';
    
    make_base(image_path);
    
    var brush_size = 8;

    $('#brush_size').change(function(e){
        var slider = document.getElementById('brush_size');
        brush_size = $(this).val();
    });
  




    function make_base(path) {
        image = new Image();
        image.src = path;


        $(image).on('load', function(){
            var pic_canvas = document.getElementById('canvas_pic');

            var width_set = 600;
            var height_set = 600 * image.height / image.width;

            pic_canvas.width = width_set;
            pic_canvas.height = height_set;

            pic_canvas.style.width = width_set;
            pic_canvas.style.height = height_set;

            var ctx = pic_canvas.getContext('2d');
            ctx.fillStyle = "rgba(255, 0, 0, 0.05)";
            
            // ctx.globalAlpha = "0.5";
            ctx.lineWidth = 0;
            ctx.globalCompositeOperation = "source-over"; 

            
            //drawImage(이미지객체, 
            //  이미지의 왼위 부분x, 이미지의 왼위 부분y, 이미지의 원하는 가로크기, 
            //  이미지의 원하는 세로크기,
            //  사각형 부분x, 사각형 부분y, 가로크기, 세로크기)
            ctx.drawImage(image, 0, 0, width_set, height_set );

            $("#original_img_url").text(path);
            $(".canvas_box, .convert_box").css('height', height_set + 70);

            
            
            
            var isDrawing, lastPoint;
              
            var result_canvas = document.getElementById('canvas_result');
            var result_ctx = result_canvas.getContext('2d');

            
            pic_canvas.onmousedown = function(e) {
                isDrawing = true;
                lastPoint = { x: e.offsetX, y: e.offsetY }; // 왼쪽 위
            };
            
            pic_canvas.onmousemove = function(e) {
                if (!isDrawing) return;
                
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
                    // ctx.stroke(); // 이거 하면 border생김
                }
                
                lastPoint = currentPoint;
            };
            
            pic_canvas.onmouseup = function() {
                isDrawing = false;
            };


            
            // diy makers Javascript
            function clearit() {
                ctx.clearRect(0,0, 1000, 1000);
                make_base(image_path);
            }
            $("#clear_btn").click(function(){
                clearit();
            });
        });

        
    }

    function sketchit(e) {
        context.beginPath()
        context.moveTo(mouseX, mouseY);
        context.lineTo(mouseX,mouseY)
        context.lineCap = 'round';
        context.lineWidth = document.getElementById('brush_size').value;
        context.strokeStyle = document.getElementById('color').value;
        context.stroke();
        MouseIsDown = true;
    };
});







function distanceBetween(point1, point2) {
    return Math.sqrt(Math.pow(point2.x - point1.x, 2) + Math.pow(point2.y - point1.y, 2));
}
function angleBetween(point1, point2) {
    return Math.atan2( point2.x - point1.x, point2.y - point1.y );
}
/*
// 캔버스 아래 이미지 깔기
function image_onCanvas(){
    var image = new Image();

    image.addEventListener('load', function(){
        var ctx = document.getElementById("canvas_pic").getContext("2d");
        ctx.drawImage(image, 0, 0,0 200, 200);
    }, false);

    image.src = "test-image/sunf.jpg";
}*/