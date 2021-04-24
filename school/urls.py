"""school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from school import settings
from management.StaffViews import *
from management.StudentViews import *
from management.EditResultViewClass import EditResultViewClass
from management.HodViews import *
from django.urls import include
from management.views import HomePage, ShowLoginPage, doLogin, GetUserDetails, logout_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', HomePage),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', ShowLoginPage, name="show_login"),
    path('get_user_details', GetUserDetails),
    path('logout', logout_user, name="logout"),
    path('admin_home', admin_home, name="admin_home"),
    path('doLogin', doLogin, name="login"),
    path('add_staff_save', add_staff_save, name="add_staff_save"),
    path('add_course', add_course, name="add_course"),
    path('manage_course', manage_course, name="manage_course"),
    path('add_course_save', add_course_save, name="add_course_save"),
    path('add_student', add_student, name="add_student"),
    path('manage_student', manage_student, name="manage_student"),
    path('add_student_save', add_student_save, name="add_student_save"),
    path('add_subject_save', add_subject_save, name="add_subject_save"),
    path('add_subject', add_subject, name="add_subject"),
    path('manage_subject', manage_subject, name="manage_subject"),    
    path('add_staff', AddStaff, name="add_staff"),
    path('manage_staff', manage_staff, name="manage_staff"),
    path('edit_staff/<str:staff_id>', edit_staff, name="edit_staff"),
    path('edit_student/<str:student_id>', edit_student, name="edit_student"),
    path('edit_staff_save', edit_staff_save, name="edit_staff_save"),
    path('edit_subject/<str:subject_id>', edit_subject, name="edit_subject"),
    path('edit_course/<str:course_id>', edit_course, name="edit_course"),
    path('edit_subject_save', edit_subject_save, name="edit_subject_save"),
    path('edit_course_save', edit_course_save, name="edit_course_save"),
    path('edit_student_save', edit_student_save, name="edit_student_save"),  
    path('manage_session', manage_session, name="manage_session"),
    path('add_session_save', add_session_save, name="add_session_save"),
    path('check_email_exist', check_email_exist,name="check_email_exist"),
    path('check_username_exist', check_username_exist,name="check_username_exist"),
    path('student_feedback_message', student_feedback_message,name="student_feedback_message"),
    path('staff_feedback_message', staff_feedback_message,name="staff_feedback_message"),
    path('student_feedback_message_replied', student_feedback_message_replied,name="student_feedback_message_replied"),
    path('staff_feedback_message_replied', staff_feedback_message_replied,name="staff_feedback_message_replied"),
    path('student_leave_view', student_leave_view,name="student_leave_view"),
    path('staff_leave_view', staff_leave_view,name="staff_leave_view"),
    path('student_approve_leave/<str:leave_id>', student_approve_leave,name="student_approve_leave"),
    path('student_disapprove_leave/<str:leave_id>', student_disapprove_leave,name="student_disapprove_leave"),
    path('staff_disapprove_leave/<str:leave_id>', staff_disapprove_leave,name="staff_disapprove_leave"),
    path('staff_approve_leave/<str:leave_id>', staff_approve_leave,name="staff_approve_leave"),
    path('admin_profile', admin_profile,name="admin_profile"),
    path('admin_profile_save', admin_profile_save,name="admin_profile_save"),
    path('student_view_result', student_view_result, name="student_view_result"),
    #staff_urls
    path('staff_home', staff_home, name="staff_home"),
    path('staff_apply_leave', staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save', staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback', staff_feedback, name="staff_feedback"),
    path('staff_feedback_save', staff_feedback_save, name="staff_feedback_save"),
    path('staff_profile', staff_profile,name="staff_profile"),
    path('staff_profile_save', staff_profile_save,name="staff_profile_save"),
    path('staff_add_result', staff_add_result, name="staff_add_result"),
    path('get_students', get_students, name="get_students"),
    path('save_student_result', save_student_result, name="save_student_result"),
    path('edit_student_result',EditResultViewClass.as_view(), name="edit_student_result"),
    path('fetch_result_student',fetch_result_student, name="fetch_result_student"),
    #student urls
    path('student_home', student_home, name="student_home"),
    path('student_apply_leave', student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save', student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback', student_feedback, name="student_feedback"),
    path('student_feedback_save', student_feedback_save, name="student_feedback_save"),
    path('student_profile', student_profile,name="student_profile"),
    path('student_profile_save', student_profile_save,name="student_profile_save"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
