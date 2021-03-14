# flask server
# Author : minku Koo
# Project Start:: 2021.03.10

from flask import Flask, request, render_template, jsonify, Blueprint, redirect, url_for
import cv2
import matplotlib.pyplot as plt
import numpy as np

server = Blueprint("server", __name__)

@server.route("/", methods=["GET"])
def index():
    print("index page!!")
    return render_template("index2.html")
    # return render_template("hello")
