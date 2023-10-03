# Image Contoller
# Author : Ji-yong219
# Project Start:: 2021.03.10.
# Last Modified from Ji-yong 2023.07.02.

from flask import (
    request,
    render_template,
    jsonify,
    Blueprint,
    redirect,
    url_for,
    session
)
import os

from ..imageProcess.imageService import (
    process_start,
    reduce_color,
    draw_line,
    numbering_sector
)

contoller = Blueprint("image_controller", __name__)


@contoller.route("/processStart", methods=["POST"])
def processStart():
    image_path = request.form['image_path']
    image_name = os.path.basename(image_path)
    image_path_o = f"{os.getcwd()}/src/main/webapp/static/org_image/{image_name}"
    image_path_r = f"{os.getcwd()}/src/main/webapp/static/render_image/{image_name}"

    target, img_name = process_start(image_name, image_path_o, image_path_r)

    return jsonify(
        target = target,
        img_name = img_name
    )


@contoller.route("/reduceColor", methods=["POST"])
def reduceColor():
    image_path = request.form['image_path']
    img_name = os.path.basename(image_path)
    image_path = f"{os.getcwd()}/src/main/webapp/static/render_image/{img_name}"

    reduce_data = request.form['reduce_data']

    clusters = [int(i) for i in reduce_data.split(',')[:3]]

    target, img_name, colorNames, colors = reduce_color(
        img_name,
        image_path,
        reduce_data,
        clusters,
    )

    session['colorNames'] = colorNames
    session['colors'] = colors

    return jsonify(
        target = target,
        img_name = img_name,
        clusters = clusters
    )


@contoller.route("/drawLine", methods=["POST"])
def drawLine():
    image_path = request.form['image_path']
    img_name = os.path.basename(image_path).split("?")[0]
    session['reduce_img_name'] = img_name
    reduce_data = request.form['reduce_data']

    colors = session['colors']
    
    target, img_name, img_lab, lab = draw_line(
        img_name,
        reduce_data,
        colors
    )

    session['img_lab'] = img_lab
    session['lab'] = lab
    session['linedraw_img_name'] = img_name

    return jsonify(
        target = target,
        img_name = img_name
    )


@contoller.route("/numbering", methods=["POST"])
def numbering():
    image_path = request.form['image_path']
    img_name = os.path.basename(image_path).split("?")[0]
    reduce_data = request.form['reduce_data']

    reduce_img_name = session['reduce_img_name']
    linedraw_img_name = session['linedraw_img_name']

    colors = session['colors']
    colorNames = session['colorNames']
    img_lab = session['img_lab']
    lab = session['lab']

    target, img_name = numbering_sector(
        reduce_img_name,
        linedraw_img_name,
        reduce_data,
        colors,
        colorNames,
        img_lab,
        lab
    )

    return jsonify(
        target = target,
        img_name = img_name
    )