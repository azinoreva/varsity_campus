""" Lecturer routes"""

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .. import db
from ..models import Lecture, User, LectureVideo, LectureDocument, Notification, Assignment, lecture_students
import json

# Blueprint for lectures
lectures_bp = Blueprint('lectures', __name__)

# View all lectures (for lecturers)
@lectures_bp.route('/lectures', methods=['GET'])
@login_required
def view_lectures():
    if not current_user.has_role('Lecturer'):
        flash('Only lecturers can view this page.')
        return redirect(url_for('courses'))
    lectures = Lecture.query.filter_by(lecturer_id=current_user.id).all()
    return render_template('lectures/view_lectures.html', lectures=lectures)

# Add a new lecture (only lecturers)
@lectures_bp.route('/lectures/create', methods=['GET','POST'])
@login_required
def create_lecture():
    # Only allow lecturers to create a lecture or add resources
    if not current_user.has_role('Lecturer'):
        flash('Only lecturers can create or manage lectures.')
        return redirect(url_for('home'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        student_emails = request.form['studentEmails']
        lecture_id = request.form['lecture_id']
        video_url=request.form['video_url']
        document_path=request.form['document_path']

        if student_emails:
            student_email_list = [mail.strip() for mail in student_emails.split(',')]

            for email in student_email_list:
                student = User.query.filter_by(email=email).first()
                if student:
                        # Check if the student is already associated with this lecture to avoid duplicates
                        exists = db.session.query(lecture_students).filter_by(
                        student_id=student.id, lecture_id=lecture_id).first()
                        if not exists:
                            # If the association does not exist, add it to lecture_students table
                            stmt = lecture_students.insert().values(
                                student_id=student.id, lecture_id=lecture_id
                            )
                            db.session.execute(stmt)
        
        lecture = Lecture.query.get_or_404(lecture_id)
        new_lecture = Lecture(title=title, description=description, lecturer_id=current_user.id)
        db.session.add(new_lecture)

        if video_url:
            video = LectureVideo(video_url, lecture_id=lecture.id)
            db.session.add(video)

        if document_path:
            document = LectureDocument(document_path, lecture_id=lecture.id)
            db.session.add(document)

        db.session.commit()
        flash('lecture created successfully.')

        return redirect(url_for('lectures.view_lectures'))

    # Render the create_lecture template if it's a GET request
    return render_template('lectures/create_lecture.html')


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

@lectures_bp.route('/lectures/<int:lecture_id>/edit', methods=['POST'])
@login_required
def edit_lecture(lecture_id):
    lectures = Lecture.query.filter_by(lecture_id)
    lectures.title = request.form['title']
    lectures.description = request.form['description']

    return render_template('lectures/view_lectures.html', lectures=lectures) 