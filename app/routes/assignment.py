from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .. import db
from ..models import Lecture, User, LectureVideo, LectureDocument, Assignment, lecture_students
from datetime import datetime

# Blueprint for lectures
assignment_bp = Blueprint('assignment', __name__)

# view assignments
@assignment_bp.route('/lecture/view_assignment/<int:lecture_id>', methods=['GET'])
@login_required
def view_assignment(lecture_id):
    assignments = Assignment.query.filter_by(lecture_id=lecture_id).all()
    return render_template('lectures/assignment.html', lecture_id=lecture_id, assignments=assignments)


# create new assignment
@assignment_bp.route('/lectures/assignment/<int:lecture_id>', methods=['GET', 'POST'])
def create_assignment(lecture_id):
    # Ensure the user is a lecturer
    if not current_user.has_role('Lecturer'):
        flash('Only lecturers can view this page.')
        return redirect(url_for('home.home'))

    # Fetch all lectures associated with the current lecturer
    lectures = Lecture.query.filter_by(lecturer_id=current_user.id).all()

    if request.method == 'POST':
        questions = request.form.get("questions")
        due_date = datetime.now()  # Assume a due date is provided

        if questions:
            # Create the assignment once
            assignment = Assignment(
                content=questions,
                due_date=due_date,
                lecturer_id=current_user.id,  # Associate with the current lecturer
                lecture_id=lecture_id
            )

            # Add the assignment to the session (before associating students)
            db.session.add(assignment)
            db.session.flush()  # Flush to get assignment.id without committing

            # Link each student in the lectures to this assignment
            with db.session.no_autoflush:  # Avoid premature flushes
                for lecture in lectures:
                    for student in lecture.students:
                        # Associate students with the assignment
                        if (student not in assignment.students):
                            assignment.students.append(student)

            # Commit all assignments and relationships at once
            db.session.commit()
            flash('Assignments created successfully.')

    return redirect(url_for('assignment.view_assignment', lecture_id=lecture_id))
