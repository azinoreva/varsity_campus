from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from ..models import Comment, CommentLike, CommentDislike, CommentRepost, Post
from .. import db


# Create a new comment on a post
@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form.get('content')

    if not content:
        return jsonify({'error': 'Comment content is required'}), 400

    post = Post.query.get_or_404(post_id)

    comment = Comment(content=content,
                      post_id=post_id,
                      user_id=current_user.id)
    db.session.add(comment)
    db.session.commit()

    return jsonify({'message': 'Comment added successfully'}), 201


# Like a comment
@app.route('/comment/<int:comment_id>/like', methods=['POST'])
@login_required
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # Check if user already liked the comment
    like = CommentLike.query.filter_by(comment_id=comment_id,
                                       user_id=current_user.id).first()
    if like:
        return jsonify({'error': 'You have already liked this comment'}), 400

    new_like = CommentLike(comment_id=comment_id, user_id=current_user.id)
    db.session.add(new_like)
    db.session.commit()

    return jsonify({'message': 'Comment liked successfully'}), 200


# Dislike a comment
@app.route('/comment/<int:comment_id>/dislike', methods=['POST'])
@login_required
def dislike_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # Check if user already disliked the comment
    dislike = CommentDislike.query.filter_by(comment_id=comment_id,
                                             user_id=current_user.id).first()
    if dislike:
        return jsonify({'error':
                        'You have already disliked this comment'}), 400

    new_dislike = CommentDislike(comment_id=comment_id,
                                 user_id=current_user.id)
    db.session.add(new_dislike)
    db.session.commit()

    return jsonify({'message': 'Comment disliked successfully'}), 200


# Repost a comment
@app.route('/comment/<int:comment_id>/repost', methods=['POST'])
@login_required
def repost_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # Check if user already reposted the comment
    repost = CommentRepost.query.filter_by(comment_id=comment_id,
                                           user_id=current_user.id).first()
    if repost:
        return jsonify({'error':
                        'You have already reposted this comment'}), 400

    new_repost = CommentRepost(comment_id=comment_id, user_id=current_user.id)
    db.session.add(new_repost)
    db.session.commit()

    return jsonify({'message': 'Comment reposted successfully'}), 200
