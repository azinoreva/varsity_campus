from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from ..models import Message, User, Channel, Reaction
from .. import db

# Send a direct message
@app.route('/message/send', methods=['POST'])
@login_required
def send_message():
    receiver_id = request.form.get('receiver_id')
    content = request.form.get('content')

    if not content:
        return jsonify({'error': 'Message content is required'}), 400

    # Check if the receiver exists
    receiver = User.query.get(receiver_id)
    if not receiver:
        return jsonify({'error': 'Receiver does not exist'}), 404

    message = Message(sender_id=current_user.id, receiver_id=receiver_id, content=content)
    db.session.add(message)
    db.session.commit()

    return jsonify({'message': 'Message sent successfully'}), 200

# Send a message to a group (channel)
@app.route('/message/channel/<int:channel_id>/send', methods=['POST'])
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
@app.route('/channel/<int:channel_id>/messages', methods=['GET'])
@login_required
def view_channel_messages(channel_id):
    channel = Channel.query.get(channel_id)
    if not channel:
        return jsonify({'error': 'Channel does not exist'}), 404

    messages = Message.query.filter_by(channel_id=channel_id).all()
    return render_template('channel_messages.html', messages=messages, channel=channel)

# View direct messages with a user
@app.route('/messages/<int:user_id>', methods=['GET'])
@login_required
def view_direct_messages(user_id):
    user = User.query.get_or_404(user_id)

    # Fetch direct messages between the current user and the selected user
    messages = Message.query.filter(
        (Message.sender_id == current_user.id) & (Message.receiver_id == user_id) |
        (Message.sender_id == user_id) & (Message.receiver_id == current_user.id)
    ).all()

    return render_template('direct_messages.html', messages=messages, user=user)

# Add a reaction to a message
@app.route('/message/<int:message_id>/react', methods=['POST'])
@login_required
def react_to_message(message_id):
    emoji = request.form.get('emoji')

    message = Message.query.get_or_404(message_id)
    reaction = Reaction(message_id=message_id, user_id=current_user.id, emoji=emoji)

    db.session.add(reaction)
    db.session.commit()

    return jsonify({'message': 'Reaction added successfully'}), 200

# Delete a message (either direct or group)
@app.route('/message/<int:message_id>/delete', methods=['DELETE'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)

    # Check if the user is authorized to delete the message (either sender or admin)
    if message.sender_id != current_user.id and not current_user.is_admin():
        return jsonify({'error': 'Unauthorized to delete this message'}), 403

    db.session.delete(message)
    db.session.commit()

    return jsonify({'message': 'Message deleted successfully'}), 200
