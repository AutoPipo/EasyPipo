# flask server
# Author : minku Koo
# Project Start:: 2021.03.10
# Last Modified from Ji-yong 2021.03.29

from flask import Flask, request, render_template, jsonify, Blueprint, redirect, url_for
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sqlite

views = Blueprint("server", __name__)

@views.route("/", methods=["GET"])
def index():
    return render_template("index.html")