"""Library route """
from flask import Blueprint render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .. import db
from ..models import LibraryItem, LibraryRequest

#Blueprint for Library
library_bp = Blueprint('library', __name__)

# Create a new library item
@library_bp.route('/library/item/create', methods=['GET', 'POST'])
@login_required
def create_library_item():
    """Route to create a new library item."""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        item_type = request.form.get('item_type')
        file = request.files.get('file')  # Handle file uploads

        if not file:
            flash('File is required to create a library item.')
            return redirect(url_for('create_library_item'))

        # Save the file and create the library item
        file_path = save_file(file)  # Function to save the file

        requires_permission = request.form.get('requires_permission') == 'on'
        permission_password = None
        if requires_permission:
            permission_password = request.form.get('permission_password')

        item = LibraryItem(
            title=title,
            description=description,
            item_type=item_type,
            file_path=file_path,
            requires_permission=requires_permission,
            permission_password=permission_password,
            owner_id=current_user.id
        )
        item.save_item()
        return redirect(url_for('library'))

    return render_template('create_library_item.html')

# Request to download a library item that requires permission
@library_bp.route('/library/item/<int:item_id>/request', methods=['POST'])
@login_required
def request_library_item(item_id):
    """Route to request a library item that requires permission."""
    item = LibraryItem.query.get_or_404(item_id)

    if item.requires_permission:
        request = LibraryRequest(item_id=item.id, requester_id=current_user.id)
        request.save_request()
        flash('Request submitted. The owner will contact you for permission.')
    else:
        flash('This item does not require permission to download.')

    return redirect(url_for('view_library_item', item_id=item_id))

# View a specific library item
@library_bp.route('/library/item/<int:item_id>', methods=['GET'])
def view_library_item(item_id):
    """Route to view details of a library item."""
    item = LibraryItem.query.get_or_404(item_id)
    return render_template('view_library_item.html', item=item)

# Delete a library item (only for super admins)
@library_bp.route('/library/item/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_library_item(item_id):
    """Route to delete a library item."""
    item = LibraryItem.query.get_or_404(item_id)

    if current_user.is_super_admin():
        db.session.delete(item)
        db.session.commit()
        flash('Library item deleted successfully.')
    else:
        flash('You do not have permission to delete this item.')

    return redirect(url_for('library'))

# List all library items
@library_bp.route('/library', methods=['GET'])
def library():
    """Route to list all library items."""
    items = LibraryItem.query.all()
    return render_template('library.html', items=items)
