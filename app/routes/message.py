from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from ..models import Message, User, Channel, ChatRoom
from .. import db

#Blueprint for message
message_bp = Blueprint ('message', __name__) 


def get_or_create_chat_room(user1_id, user2_id):
    # Ensure chat rooms are unique between two users regardless of the order
    chat_room = ChatRoom.query.filter(
        ((ChatRoom.user1_id == user1_id) & (ChatRoom.user2_id == user2_id)) |
        ((ChatRoom.user1_id == user2_id) & (ChatRoom.user2_id == user1_id))
    ).first()

    if not chat_room:
        # If no chat room exists, create a new one
        chat_room = ChatRoom(user1_id=user1_id, user2_id=user2_id)
        db.session.add(chat_room)
        db.session.commit()

    return chat_room

# Send a direct message
@message_bp.route('/send_message/<int:user_id>', methods=['POST'])
@login_required
def send_message(user_id):
    receiver_id = request.form.get('receiver_id')
    user = User.query.get_or_404(user_id)
    content = request.form.get('content')

    # Check if the user is a friend
    if user not in current_user.friends:
        flash("You can only send messages to friends.", "danger")
        return redirect(url_for('dashboard.friend'))

    chat_room = get_or_create_chat_room(current_user.id, receiver_id)

    message = Message(sender_id=current_user.id, receiver_id=receiver_id, content=content, chat_room_id=chat_room.id)
    db.session.add(message)
    db.session.commit()

    return redirect(url_for('message.view_direct_messages', user_id=receiver_id))

# Send a message to a group (channel)
@message_bp.route('/message/channel/<int:channel_id>/send', methods=['POST'])
@login_required
def send_channel_message(channel_id):
    content = request.form.get('content')

    if not content:
        return jsonify({'error': 'Message content is required'}), 400

    channel = Channel.query.get(channel_id)
    if not channel:
        return jsonify({'error': 'Channel does not exist'}), 404

    message = Message(sender_id=current_user.id, channel_id=channel_id, content=content)
    db.session.add(message)
    db.session.commit()

    return jsonify({'message': 'Message sent successfully'}), 200

# View messages in a channel
@message_bp.route('/channel/<int:channel_id>/messages', methods=['GET'])
@login_required
def view_channel_messages(channel_id):
    channel = Channel.query.get(channel_id)
    if not channel:
        return jsonify({'error': 'Channel does not exist'}), 404

    messages = Message.query.filter_by(channel_id=channel_id).all()
    return render_template('channel_messages.html', messages=messages, channel=channel)

# View direct messages with a user
@message_bp.route('/messages/<int:user_id>', methods=['GET'])
@login_required
def view_direct_messages(user_id):
    user = User.query.get_or_404(user_id)

    if user not in current_user.friends:
        flash("You can only message friends.", "danger")
        return redirect(url_for('dashboard.friend'))
    
    chat_room = get_or_create_chat_room(current_user.id, user_id)

    # Fetch direct messages between the current user and the selected user
    messages = Message.query.filter_by(chat_room_id=chat_room.id).order_by(Message.sent_at.asc()).all()

    return render_template('direct_messages.html', messages=messages, user=user)

# Add a reaction to a message
@message_bp.route('/message/<int:message_id>/react', methods=['POST'])
@login_required
def react_to_message(message_id):
    emoji = request.form.get('emoji')

    message = Message.query.get_or_404(message_id)
    reaction = Reaction(message_id=message_id, user_id=current_user.id, emoji=emoji)

    db.session.add(reaction)
    db.session.commit()

    return jsonify({'message': 'Reaction added successfully'}), 200

# Delete a message (either direct or group)
@message_bp.route('/message/<int:message_id>/delete', methods=['DELETE'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)

    # Check if the user is authorized to delete the message (either sender or admin)
    if message.sender_id != current_user.id and not current_user.is_admin():
        return jsonify({'error': 'Unauthorized to delete this message'}), 403

    db.session.delete(message)
    db.session.commit()

    return jsonify({'message': 'Message deleted successfully'}), 200
