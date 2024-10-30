from flask import Blueprint, render_template, url_for, request, redirect, current_app, flash
from flask_login import login_required, current_user
import os
from ..models import User, friends, Post, Lecture
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
        redirect(url_for('dashboard.profile', user_id=user.id, current_user=current_user))

    posts = Post.query.filter_by(user_id=user.id).all()  # Get all posts by the user
    lectures = Lecture.query.filter(Lecture.students.any(id=user.id)).all()

    return render_template('dashboard.html', user=user, posts=posts, lectures=lectures)

# handles adding another user as a friend
@login_required
@dashboard_bp.route('/add_friend/<int:friend_id>', methods=['POST'])
def add_friend(friend_id):
    friend = User.query.get(friend_id)
    
    if friend and friend.id != current_user.id:
        current_user.friends.append(friend)
        db.session.commit()
        flash(f'You are now friends with {friend.username}!', 'success')
    else:
        flash('You cannot add yourself as a friend.', 'danger')

    return redirect(url_for('dashboard.profile', user_id=friend_id))


# display all the friends a user has
@login_required
@dashboard_bp.route('/friends', methods=['GET'])
def friend():
    friends_list = current_user.friends.all()

    return render_template("friends.html", friends=friends_list)