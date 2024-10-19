from flask import Blueprint, render_template

# Blueprint for home page
home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')