from flask import Blueprint, render_template


HOME = Blueprint('home', __name__)


@HOME.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
