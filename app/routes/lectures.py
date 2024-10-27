""" Lecturer routes"""

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .. import db
from ..models import Lecture, User, LectureVideo, LectureDocument, Notification, Assignment, lecture_students
import json

# Blueprint for lectures
lectures_bp = Blueprint('lectures', __name__)

# View all lectures (for lecturers)
@lectures_bp.route('/lectures/<int:lecturer_id>', methods=['GET'])
@login_required
def view_lectures(lecturer_id):
    if not current_user.has_role('Lecturer'):
        flash('Only lecturers can view this page.')
        return redirect(url_for('courses'))
    lectures = Lecture.query.filter_by(lecturer_id=lecturer_id).all()
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
        # video_url = request.form['video_url']
        # document_path = request.form['document_path']

        new_lecture = Lecture(title=title, description=description, lecturer_id=current_user.id)
        db.session.add(new_lecture)
        db.session.commit()

        lecture_id = new_lecture.id

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

        # if video_url:
        #     video = LectureVideo(video_url, lecture_id=lecture.id)
        #     db.session.add(video)

        # if document_path:
        #     document = LectureDocument(document_path, lecture_id=lecture.id)
        #     db.session.add(document)

        db.session.commit()
        flash('lecture created successfully.')

        return redirect(url_for('lectures.view_lectures', lecturer_id=new_lecture.lecturer_id))

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

from flask import abort

@lectures_bp.route('/lectures/edit/<int:lecture_id>', methods=['GET', 'POST'])
def edit_lecture(lecture_id):
    # Ensure only lecturers can edit a lecture
    if not current_user.has_role('Lecturer'):
        flash('Only lecturers can edit lectures.')
        return redirect(url_for('home'))

    # Fetch the lecture by ID
    lecture = Lecture.query.get_or_404(lecture_id)

    if request.method == 'POST':
        # Update the lecture's title and description
        lecture.title = request.form['title']
        lecture.description = request.form['description']
        
        # Update student associations if emails are provided
        student_emails = request.form.get('studentEmails')
        if student_emails:
            student_email_list = [mail.strip() for mail in student_emails.split(',')]
            
            # Remove existing associations for students not in the new list
            lecture_students_to_keep = []
            for email in student_email_list:
                student = User.query.filter_by(email=email).first()
                if student:
                    exists = db.session.query(lecture_students).filter_by(
                        student_id=student.id, lecture_id=lecture_id).first()
                    if not exists:
                        stmt = lecture_students.insert().values(
                            student_id=student.id, lecture_id=lecture_id
                        )
                        db.session.execute(stmt)
                    lecture_students_to_keep.append(student.id)

            # Remove students who are no longer associated
            db.session.query(lecture_students).filter(
                lecture_students.c.lecture_id == lecture_id,
                ~lecture_students.c.student_id.in_(lecture_students_to_keep)
            ).delete(synchronize_session=False)

        # Commit changes to the database
        db.session.commit()
        flash('Lecture updated successfully.')
        return redirect(url_for('lectures.view_lectures',lecturer_id=lecture.lecturer_id))

    # Render the edit lecture template with existing data if it's a GET request
    return render_template('lectures/edit_lecture.html', lecture_id=lecture_id, lecture=lecture)


@lectures_bp.route('/lectures/delete/<int:lecture_id>', methods=['DELETE','POST'])
def delete_lecture(lecture_id):
    # Ensure only lecturers can delete a lecture
    if not current_user.has_role('Lecturer'):
        flash('Only lecturers can delete lectures.')
        return redirect(url_for('home'))

    # Fetch the lecture to delete by ID
    lecture = Lecture.query.get_or_404(lecture_id)

    # Delete the lecture and associated data
    db.session.delete(lecture)
    db.session.commit()
    
    flash('Lecture deleted successfully.')
    return redirect(url_for('lectures.view_lectures'))
