from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .. import db, utils
from app.models import Community, User
from app.models.community import CommunityMessage 
from sqlalchemy.orm import joinedload

# Blueprint for community routes
community_bp = Blueprint('community', __name__)

# View all communities with optional search functionality
@community_bp.route('/communities', methods=['GET'])
@login_required
def view_communities():
    search_query = request.args.get('search')
    
    if search_query:
        communities = Community.query.filter(
            Community.name.ilike(f'%{search_query}%') |
            Community.description.ilike(f'%{search_query}%')
        ).all()
    else:
        communities = Community.query.all()

    return render_template('communities.html', communities=communities, search_query=search_query)

# Join a community
@community_bp.route('/community/join/<int:community_id>', methods=['POST'])
@login_required
def join_community(community_id):
    community = Community.query.get_or_404(community_id)

    # Check if user is already a member
    if current_user in community.members:
        flash('You are already a member of this community.')
        return redirect(url_for('community.view_communities'))

    community.members.append(current_user)
    db.session.commit()
    flash(f'You have joined the community: {community.name}')
    return redirect(url_for('community.view_communities'))

# Leave a community
@community_bp.route('/community/leave/<int:community_id>', methods=['POST'])
@login_required
def leave_community(community_id):
    community = Community.query.get_or_404(community_id)

    # Check if user is a member
    if current_user not in community.members:
        flash('You are not a member of this community.')
        return redirect(url_for('community.view_communities'))

    community.members.remove(current_user)
    db.session.commit()
    flash(f'You have left the community: {community.name}')
    return redirect(url_for('community.view_communities'))

 # View specific community and its messages
@community_bp.route('/community/<int:community_id>', methods=['GET', 'POST'])
@login_required
def view_community_detail(community_id):
    community = Community.query.get_or_404(community_id)
    messages = CommunityMessage.query.options(joinedload(CommunityMessage.user)).filter_by(community_id=community_id).all()

    # Handle posting a message
    if request.method == 'POST':
        content = request.form.get('content')
        file = request.files.get('file')

        if not content and not file:
            flash('You must provide either a message or a file.')
            return redirect(url_for('community.view_community_detail', community_id=community_id))

        filename = None
        if file:
            filename = utils.save_file(file)

        new_message = CommunityMessage(
            user_id=current_user.id,
            community_id=community_id,
            message=content,
            file_url=filename
        )

        db.session.add(new_message)
        db.session.commit()

        flash('Your message has been posted.')
        return redirect(url_for('community.view_community_detail', community_id=community_id))

    return render_template('inside_communities.html', community=community, messages=messages)
