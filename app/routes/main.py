from flask import Blueprint, render_template
from app.routes.auth import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
