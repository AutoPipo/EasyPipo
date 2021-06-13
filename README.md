# Easy Pipo
## "Pipo Painting" Auto Creation System

<h3 align="center">Our Icon</h3>
<p align="center">
  <img src="/about_project/logo.png" width="25%" title="logo"></img>
</p><br>

📌 Authors : [Minku Koo](https://github.com/Minku-Koo) &nbsp; [Jiyong Park](https://github.com/Ji-yong219)    
📌 Period : Feb.2021 ~ Jun.2021   
📌 Keyword : "Computer Vision", "Image Processing", "OpenCV", "Pipo Painting", "Line Detection", "Color Numbering"    


## ⚙ Our System is...
### Using Image Processing, the real image is automatically converted to a "Pipo Painting" canvas.

## 🤔 What is Pipo Painting?
<img src="/about_project/pipo-example.jpg" width="40%" title="pipopainting-example" style="float: left" ></img> 
"Pipo Painting" is also called "Paint by Number" or "Painting by Numbers".    
It is a kit having a board on which light markings to indicate areas to paint, and each area has a number and a corresponding numbered paint to use. The kits come with little compartmentalised boxes where the numbered colour pigments are stored. The users are encouraged to wash the paintbrush every time a new numbered colour is being used. The kits were invented, developed and marketed in 1950 by Max S. Klein, an engineer and owner of the Palmer Paint Company of Detroit, Michigan, and Dan Robbins, a commercial artist.

[Wikipedia Discription](https://en.wikipedia.org/wiki/Paint_by_number)   
[Search on Amazon](https://www.amazon.com/Pipo-Painting/s?k=Pipo+Painting)   

## 🛠💡 Working Steps

<h3  align="center">Original Image</h3>
<p align="center">
  <img src="/about_project/test-image/lala.jpg" width="50%" title="original"></img>
</p>

<h3 align="center" >Step 1. Color Clustering (8, 16, 32 Colors)</h3>
<!--<h3  align="center">8 Colors&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  16 Colors&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  32 Colors
</h3>-->
<p align="center">
  <img src="/about_project/test-image/lala-color-8.jpg" width="30%" title="8 colors" ></img>
  <img src="/about_project/test-image/lala-color-16.jpg" width="30%" title="16 colors"></img>
  <img src="/about_project/test-image/lala-color-32.jpg" width="30%" title="32 colors"></img>
</p>

<h3 align="center" >Step 2. Select appropriate number of colors and Line Drawing</h3>
<p align="center">
  <img src="/about_project/test-image/lala-lainedraw.jpg" width="50%" title="line drawing"></img>
</p>

<h3 align="center" >Step 3. Remove noise line and Set Color Numbering (Color Label Included or Not)</h3>
<!--<h3  align="center">Color Label Included&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Unincluded
</h3>-->
<p align="center">
  <img src="/about_project/test-image/lala-numbering-label.jpg" width="40%" title="numbering+label"></img>
  <img src="/about_project/test-image/lala-numbering.jpg" width="40%" title="numbering+non_label"></img>
</p>

<h3 align="center" >You can see Number</h3>
<p align="center">
  <img src="/about_project/test-image/lala-numbering-expand.jpg" width="50%" title="numbering-expand"></img>
</p>

## 📚 Python Modules

### 📍 Painting()

### 📍 DrawLine()

### 📍 Numbering()

## 📧 Contact
- corleone@kakao.com
- wldydslapjyy@naver.com 

