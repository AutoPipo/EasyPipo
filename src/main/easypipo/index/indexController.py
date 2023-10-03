# index controller
# Author : Ji-yong219
# Project Start:: 2021.03.10.
# Last Modified from Ji-yong 2023.06.22.

from flask import request, render_template, jsonify, Blueprint, redirect, url_for, session, current_app
import os


contoller = Blueprint("server", __name__)


@contoller.route("/", methods=["GET"])
def index():
    return render_template("index.html")
    
@contoller.route("/whatIsPipo", methods=["GET"])
def whatIsPipo():
    return render_template("what_is_pipo.html")
    
@contoller.route("/howToUse", methods=["GET"])
def howToUse():
    return render_template("how_to_use.html")
    
@contoller.route("/colorSetting", methods=["GET"])
def ColorSetting():
    return render_template("color_setting.html")

@contoller.route("/uploadIMG", methods=["POST"])
def upload_img():
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('file')

    errors = {}
    success = False
    filepath = None

    for file in files:
        if file:
            # filename = secure_filename(file.filename) # secure_filename은 한글명을 지원하지 않음
            filename = file.filename 
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            filepath = filepath.replace("\\", "/")
            
            # file save (with uploaded)
            file.save(filepath)
            success = True

        else:
            errors[file.filename] = 'File type is not allowed'
    
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 206
        return resp

    # main 
    if success:
        resp = jsonify({'message' : 'Files successfully uploaded'})
        resp.status_code = 201
        return resp

    else:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp
