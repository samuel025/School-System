from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from management.models import CustomUser, Staffs, Courses, StudentAssignments, SessionYearModel, Subjects, Students, LeaveReportStudent, StudentResult, FeedBackStudent

def student_home(request):
    student_obj=Students.objects.get(admin=request.user.id)
    course=Courses.objects.get(id=student_obj.course_id.id)
    subjects=Subjects.objects.filter(course_id=course).count()
    leave_count=LeaveReportStudent.objects.filter(student_id=student_obj.id,leave_status=1).count()
    return render(request, "student_template/student_home.html", {"subjects":subjects, "student":student_obj, "leave":leave_count})

def student_apply_leave(request):
    staff_obj = Students.objects.get(admin=request.user.id)
    leave_data=LeaveReportStudent.objects.filter(student_id=staff_obj)
    return render(request,"student_template/student_apply_leave.html",{"leave_data":leave_data})

def student_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStudent(student_id=student_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))


def student_feedback(request):
    staff_id=Students.objects.get(admin=request.user.id)
    feedback_data=FeedBackStudent.objects.filter(student_id=staff_id)
    return render(request,"student_template/student_feedback.html",{"feedback_data":feedback_data})

def student_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackStudent(student_id=student_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))

def student_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    student=Students.objects.get(admin=user)
    return render(request,"student_template/student_profile.html",{"user":user,"student":student})

def student_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            student=Students.objects.get(admin=customuser)
            student.address=address
            student.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("student_profile"))

def student_view_result(request):
    session_year = SessionYearModel.objects.all().order_by("-id")
    student = Students.objects.get(admin=request.user.id)
    studentresult = StudentResult.objects.filter(student_id=student.id)
    return render(request, "student_template/student_result.html", {"studentresult":studentresult, "student":student, "session":session_year})

def view_result(request, session_id):
    student = Students.objects.get(admin=request.user.id)
    studentresult = StudentResult.objects.filter(student_id=student.id).filter(session_year_id=session_id)
    student_result_class = StudentResult.objects.filter(student_id=student.id).filter(session_year_id=session_id).first()
    return render(request, "student_template/view_student_result.html", {"studentresult":studentresult, "student_class":student_result_class})

def view_assignments(request):
    student_obj=Students.objects.get(admin=request.user.id)
    course=Courses.objects.get(id=student_obj.course_id.id)
    studentassignment = StudentAssignments.objects.filter(course_id=course)
    return render(request, "student_template/view_assignment.html", {"assignment":studentassignment})