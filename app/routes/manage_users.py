from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import User
from .. import db
from ..models.user import Role

manage_users_bp = Blueprint('manage_users', __name__)

# Admin route to list all users
@manage_users_bp.route('/manage_users/users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if not current_user.is_super_admin():
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('auth.login'))

    users = User.query.all()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                try:
                    current_user.assign_lecturer(user)
                    db.session.commit()
                    flash(f'{user.username} has been assigned the Lecturer role.', 'success')
                except ValueError as e:
                    flash(str(e), 'danger')
            else:
                flash('User not found.', 'danger')
        else:
            flash('Invalid user ID.', 'danger')

        return redirect(url_for('manage_users.manage_users'))

    return render_template('manage_users.html', users=users)
