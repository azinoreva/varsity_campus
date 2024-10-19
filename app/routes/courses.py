"""Course Route"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .. import db
from ..models import Course

# Blueprint for course manager
courses_bp = Blueprint('courses', __name__)

# View assignments and notifications
@courses_bp.route('/courses', methods=['GET'])
@login_required
def view_courses():
    # Get all courses for the current student
    courses = Course.query.filter_by(student_id=current_user.id).all()
    return render_template('courses.html', courses=courses)

# Mark assignment as done
@courses_bp.route('/course/<int:course_id>/mark_done', methods=['POST'])
@login_required
def mark_assignment_done(course_id):
    course = Course.query.get_or_404(course_id)
    if course.student_id != current_user.id:
        flash('You are not authorized to mark this assignment.')
        return redirect(url_for('courses.view_courses'))
    course.marked_done = True
    db.session.commit()
    flash('Assignment marked as done.')
    return redirect(url_for('courses.view_courses'))

# Submit an assignment
@courses_bp.route('/course/<int:course_id>/submit', methods=['POST'])
@login_required
def submit_assignment(course_id):
    course = Course.query.get_or_404(course_id)
    if course.student_id != current_user.id:
        flash('You are not authorized to submit this assignment.')
        return redirect(url_for('courses.view_courses'))

    # Assuming you handle file upload for assignment submission
    # Here, you would handle the submission logic.
    course.submitted = True
    course.submitted_at = datetime.utcnow()  # Set submission timestamp
    db.session.commit()
    flash('Assignment submitted successfully.')
    return redirect(url_for('courses.view_courses'))

# View notifications related to assignments
@courses_bp.route('/course/<int:course_id>/notifications', methods=['GET'])
@login_required
def view_notifications(course_id):
    course = Course.query.get_or_404(course_id)
    if course.student_id != current_user.id:
        flash('You are not authorized to view notifications for this assignment.')
        return redirect(url_for('courses.view_courses'))

    # Get notifications related to the assignment
    notifications = course.assignment.lecture.notifications
    return render_template('courses/view_notifications.html', notifications=notifications)
