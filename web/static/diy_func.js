// diy makers Javascript
function clearit() {
    ctx.clearRect(0,0, 1000, 1000);
}

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