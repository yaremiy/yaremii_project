from flask import render_template, request, redirect, url_for
from datetime import datetime
import os
from . import home_bp

@home_bp.route('/')
def index():
    return render_template("main.html",
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


@home_bp.route("/about")
def about():
    return render_template("about.html",
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


@home_bp.route("/certifications")
def certifications():
    return render_template("certifications.html",
                           operating_system=os.name,
                           user_agent=request.user_agent,
                           time=datetime.now().strftime("%H:%M:%S"))


@home_bp.route("/portfolio")
def portfolio():
    return redirect(url_for('home.index'))
