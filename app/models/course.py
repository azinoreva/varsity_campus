"""Course Model"""

# Course Model
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # The student who owns the course
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)  # Assignment reference
    submitted = db.Column(db.Boolean, default=False)  # Track if the assignment was submitted
    marked_done = db.Column(db.Boolean, default=False)  # Track if the assignment was marked done
    submitted_at = db.Column(db.DateTime, nullable=True)  # Time of submission

    assignment = db.relationship('Assignment', backref='courses')  # Relationship to Assignment
