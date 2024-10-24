from app import create_app, db
from app.models.user import User
from app.models.user import Role

app = create_app()

with app.app_context():
    # Create the Super Admin role if it doesn't exist
    super_admin_role = Role.query.filter_by(name='Super Admin').first()
    if not super_admin_role:
        super_admin_role = Role(name='Super Admin')
        db.session.add(super_admin_role)
        db.session.commit()

    # Create a super admin user
    super_admin = User(username='superadmin', email='superadmin@varsitycampus.com')
    super_admin.set_password('thisisvarsitycampus')

    # Assign the Super Admin role
    super_admin.roles.append(super_admin_role)
    db.session.add(super_admin)
    db.session.commit()
