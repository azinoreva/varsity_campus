from flask import render_template, redirect, url_for, request, flash
from flask import Blueprint
from flask_login import login_required, current_user
from .. import db, utils
from ..models import Post, Like, Comment, Repost

# Create a new post
posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')
        image = request.files.get('image')  # Handle image uploads
        if len(text) > 2000:
            flash('Text exceeds the 2000-character limit.')
            return redirect(url_for('posts.create_post'))

        # Save image and create post
        image_path = None
        if image:
            image_path = utils.save_image(image)  # Function to save the image file

        post = Post(text=text, image=image_path, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('create_post.html')

# Like a post
@posts_bp.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if existing_like:
        flash('You have already liked this post.')
        return redirect(url_for('posts.view_a_post', post_id=post_id))

    like = Like(user_id=current_user.id, post_id=post_id)
    db.session.add(like)
    db.session.commit()
    return redirect(url_for('posts.view_a_post', post_id=post_id))

# View a post
@posts_bp.route('/post/<int:post_id>', methods=['GET'])
def view_a_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.views += 1  # Increment views
    db.session.commit()
    return render_template('view_post.html', post=post)

# Search for a post
@posts_bp.route('/post/search', methods=['GET'])
def search_posts():
    query = request.args.get('q')  
    if query:
        posts = Post.query.filter(
            (Post.title.ilike(f'%{query}%')) | (Post.text.ilike(f'%{query}%'))
        ).all()
        return render_template('search_results.html', posts=posts)
    else:
        flash("Please enter a search term.", "warning")
        return redirect(url_for('posts.view_posts'))

@posts_bp.route('/posts', methods=['GET'])
@login_required
def view_posts():
    """Route to list all post items."""
    items = Post.query.all()
    return render_template('posts.html', items=items)

# Comment on a post
@posts_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def comment_post(post_id):
    text = request.form.get('text')
    if len(text) > 500:
        flash('Comment exceeds the 500-character limit.')
        return redirect(url_for('posts.view_a_post', post_id=post_id))

    post = Post.query.get_or_404(post_id)
    comment = Comment(text=text, user_id=current_user.id, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('posts.view_a_post', post_id=post_id))

# Repost functionality
@posts_bp.route('/post/<int:post_id>/repost', methods=['POST'])
@login_required
def repost(post_id):
    post = Post.query.get_or_404(post_id)
    repost = Repost(user_id=current_user.id, post_id=post_id)
    db.session.add(repost)
    db.session.commit()
    return redirect(url_for('posts.view_a_post', post_id=post_id))

# Delete a post
@posts_bp.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('profile', user_id=post.user_id))
