""" Lecturer routes"""

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .. import db
from .models import Lecture, User, LectureVideo, LectureDocument, Assignment, Notification

# Blueprint for lectures
lectures_bp = Blueprint('lectures', __name__)

# View all lectures (for lecturers)
@lectures_bp.route('/lectures', methods=['GET'])
@login_required
def view_lectures():
    if not current_user.has_role('Lecturer'):
        flash('Only lecturers can view this page.')
        return redirect(url_for('home'))
    lectures = Lecture.query.filter_by(lecturer_id=current_user.id).all()
    return render_template('lectures/view_lectures.html', lectures=lectures)

# Add a new lecture (only lecturers)
@lectures_bp.route('/lectures/create', methods=['GET', 'POST'])
@login_required
def create_lecture():
    if not current_user.has_role('Lecturer'):
        flash('Only lecturers can create lectures.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_lecture = Lecture(title=title, description=description, lecturer_id=current_user.id)
        db.session.add(new_lecture)
        db.session.commit()
        flash('Lecture created successfully.')
        return redirect(url_for('lectures.view_lectures'))
    return render_template('lectures/create_lecture.html')

# Add a student to a lecture
@lectures_bp.route('/lectures/<int:lecture_id>/add_student', methods=['POST'])
@login_required
def add_student_to_lecture(lecture_id):
    if not current_user.has_role('Lecturer'):
        flash('Only lecturers can add students to lectures.')
        return redirect(url_for('home'))
    lecture = Lecture.query.get_or_404(lecture_id)
    student_id = request.form['student_id']
    student = User.query.get(student_id)
    if student:
        lecture.students.append(student)
        db.session.commit()
        flash('Student added to lecture.')
    return redirect(url_for('lectures.view_lectures'))

# Add video or document to a lecture
@lectures_bp.route('/lectures/<int:lecture_id>/add_resource', methods=['POST'])
@login_required
def add_resource_to_lecture(lecture_id):
    if not current_user.has_role('Lecturer'):
        flash('Only lecturers can add resources to lectures.')
        return redirect(url_for('home'))
    lecture = Lecture.query.get_or_404(lecture_id)
    if 'video_url' in request.form:
        video = LectureVideo(video_url=request.form['video_url'], lecture_id=lecture.id)
        db.session.add(video)
    if 'document_path' in request.form:
        document = LectureDocument(document_path=request.form['document_path'], lecture_id=lecture.id)
        db.session.add(document)
    db.session.commit()
    flash('Resource added to lecture.')
    return redirect(url_for('lectures.view_lectures'))

# Send notification to students
@lectures_bp.route('/lectures/<int:lecture_id>/notify', methods=['POST'])
@login_required
def notify_students(lecture_id):
    if not current_user.has_role('Lecturer'):
        flash('Only lecturers can send notifications.')
        return redirect(url_for('home'))
    lecture = Lecture.query.get_or_404(lecture_id)
    notification = Notification(message=request.form['message'], lecture_id=lecture.id)
    db.session.add(notification)
    db.session.commit()
    flash('Notification sent.')
    return redirect(url_for('lectures.view_lectures'))

# Drop assignment for students
@lectures_bp.route('/lectures/<int:lecture_id>/drop_assignment', methods=['POST'])
@login_required
def drop_assignment(lecture_id):
    if not current_user.has_role('Lecturer'):
        flash('Only lecturers can drop assignments.')
        return redirect(url_for('home'))
    lecture = Lecture.query.get_or_404(lecture_id)
    assignment = Assignment(description=request.form['description'], due_date=request.form['due_date'], lecture_id=lecture.id)
    db.session.add(assignment)
    db.session.commit()
    flash('Assignment dropped.')
    return redirect(url_for('lectures.view_lectures'))
