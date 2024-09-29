from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .. import db
from .models import Community, User

# Blueprint for community routes
community_bp = Blueprint('community', __name__)

# View all communities
@community_bp.route('/communities', methods=['GET'])
@login_required
def view_communities():
    communities = Community.query.all()
    return render_template('view_communities.html', communities=communities)

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
