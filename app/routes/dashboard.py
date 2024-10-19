from flask import Blueprint, render_template, url_for, request, redirect, current_app, flash
from flask_login import login_required
import os
from ..models import User
from ..utils import save_image, delete_file
from .. import db

dashboard_bp = Blueprint('dashboard', __name__)

@login_required
@dashboard_bp.route('/profile/<int:user_id>', methods=['GET','POST'])
def profile(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        # update bio
        if 'bio' in request.form:
            user.bio = request.form['bio']
        
        # handle profile picture update
        if 'profile_image' in request.files:
            profile_image = request.files['profile_image']
            if profile_image:
                if user.profile_image:
                    old_image_path = os.path.join(current_app.root_path, 'static/images', user.profile_image)
                    delete_file(old_image_path)
                
                # save new profile picture
                new_filename = save_image(profile_image)
                user.profile_image = new_filename

        db.session.commit()
        flash('profile updated successfully', 'success')
        redirect(url_for('dashboard.profile', user_id=user.id))

    # posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user)