from django import forms

from django.forms import ChoiceField
from .models import Courses, SessionYearModel, Subjects, StudentResult

class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass

class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)
        self.fields['course'].choices = [(c.id, c.course_name) for c in Courses.objects.all()]

    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    course_list = []
    try:
        courses = Courses.objects.all()
        for course in courses:
            small_course = (course.id, course.course_name)
            course_list.append(small_course)
    except:
        course_list =[]
    
    session_list = []

    
    try:
        sessions = SessionYearModel.objects.all()
        for session in sessions:
            small_session = (session.id, str(session.session_start_year)+" TO "+str(session.session_end_year)+"("+(session.session_term)+")") 
            session_list.append(small_session)
    except:
        session_list =[]
        
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )

    course = forms.ChoiceField(label="Class", widget=forms.Select(attrs={"class":"form-control"}))
    sex = forms.ChoiceField(label="Sex", choices=gender_choice, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", widget=forms.Select(attrs={"class":"form-control"}), choices=session_list)
    profile_pic = forms.FileField(label="Profile Picture", widget=forms.FileInput(attrs={"class":"form-control"}))
    
    
   

class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    
    course_list = []
    try:
        courses = Courses.objects.all()
        for course in courses:
            small_course = (course.id, course.course_name)
            course_list.append(small_course)
    except:
        course_list = []
    
    session_list = []
    try:
        sessions = SessionYearModel.objects.all()
        for session in sessions:
            small_session = (session.id, str(session.session_start_year)+" - "+str(session.session_end_year))
            session_list.append(small_session)
    except:
        session_list =[]
    
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )

    course = forms.ChoiceField(label="Class", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    sex = forms.ChoiceField(label="Sex", choices=gender_choice, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", widget=forms.Select(attrs={"class":"form-control"}), choices=session_list)
    profile_pic = forms.FileField(label="Profile Picture",required=False, widget=forms.FileInput(attrs={"class":"form-control"}))


class EditResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.staff_id=kwargs.pop("staff_id")
        super(EditResultForm, self).__init__(*args, **kwargs)
    
        subject_list = []
        try:
            subjects = Subjects.objects.filter(staff_id=self.staff_id)
            for subject in subjects:
                subject_single = (subject.id, str(subject.subject_name) +" "+ str(subject.course_id.course_name))
                subject_list.append(subject_single)
        except:
            subject_list = []

        self.fields['subject_id'].choices=subject_list


    session_list = []
    try:
        sessions = SessionYearModel.objects.all()
        for session in sessions:
            session_single = (session.id, str(session.session_start_year) + " to "+str(session.session_end_year))
            session_list.append(session_single)
    except:
        session_list = []
    

    subject_id = forms.ChoiceField(label="Subject", widget=forms.Select(attrs={"class":"form-control"}))
    session_ids = forms.ChoiceField(label="Session Year", choices=session_list, widget=forms.Select(attrs={"class":"form-control"}))
    student_ids = ChoiceNoValidation(label="Student", widget=forms.Select(attrs={"class":"form-control"}))
    assignment_marks = forms.CharField(label="Assignment Marks", widget=forms.TextInput(attrs={"class":"form-control"}))
    exam_marks = forms.CharField(label="Exam Marks", widget=forms.TextInput(attrs={"class":"form-control"}))

