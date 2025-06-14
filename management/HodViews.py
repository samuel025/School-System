from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from management.models import *
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from management.forms import AddStudentForm, EditStudentForm

def admin_home(request):
    student_count1=Students.objects.all().count()
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.all().count()
    course_count=Courses.objects.all().count()

    course_all=Courses.objects.all()
    course_name_list=[]
    subject_count_list=[]
    student_count_list_in_course=[]
    for course in course_all:
        subjects=Subjects.objects.filter(course_id=course.id).count()
        students=Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all=Subjects.objects.all()
    subject_list=[]
    student_count_list_in_subject=[]
    for subject in subjects_all:
        course=Courses.objects.get(id=subject.course_id.id)
        student_count=Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    # staffs=Staffs.objects.all()
    # attendance_present_list_staff=[]
    # attendance_absent_list_staff=[]
    # staff_name_list=[]
    # for staff in staffs:
    #     subject_ids=Subjects.objects.filter(staff_id=staff.admin.id)
    #     attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
    #     leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
    #     attendance_present_list_staff.append(attendance)
    #     attendance_absent_list_staff.append(leaves)
    #     staff_name_list.append(staff.admin.username)

    # students_all=Students.objects.all()
    # attendance_present_list_student=[]
    # attendance_absent_list_student=[]
    # student_name_list=[]
    # for student in students_all:
    #     attendance=AttendanceReport.objects.filter(student_id=student.id,status=True).count()
    #     absent=AttendanceReport.objects.filter(student_id=student.id,status=False).count()
    #     leaves=LeaveReportStudent.objects.filter(student_id=student.id,leave_status=1).count()
    #     attendance_present_list_student.append(attendance)
    #     attendance_absent_list_student.append(leaves+absent)
    #     student_name_list.append(student.admin.username)


    return render(request,"hod_template/home_content.html",{"student_count":student_count1,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count,"course_name_list":course_name_list,"subject_count_list":subject_count_list,"student_count_list_in_course":student_count_list_in_course,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list})


def AddStaff(request):
    return render(request, "hod_template/add_staff.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

def add_course(request):
    return render(request, "hod_template/add_course.html")

def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course = request.POST.get("course")
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Class added sucessfully")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request, "Failed to add Class")
            return HttpResponseRedirect(reverse("add_course"))

def add_student(request):
    courses = Courses.objects.all()
    form = AddStudentForm()
    return render(request, "hod_template/add_student.html", {"form":form})

def add_student_save(request):
        if request.method!="POST":
            return HttpResponse("Method Not Allowed")
        else:
            form = AddStudentForm(request.POST, request.FILES)
            if form.is_valid():
                first_name=form.cleaned_data["first_name"]
                last_name=form.cleaned_data["last_name"]
                username=form.cleaned_data["username"]
                email=form.cleaned_data["email"]
                password=form.cleaned_data["password"]
                address=form.cleaned_data["address"]
                sex=form.cleaned_data["sex"]
                course_id=form.cleaned_data["course"]
                session_year_id=form.cleaned_data["session_year_id"]
                profile_pic=request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name,profile_pic)
                profile_pic_url = fs.url(filename)

                try:
                    user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                    user.students.address=address
                    course_obj=Courses.objects.get(id=course_id)
                    session_year = SessionYearModel.objects.get(id=session_year_id)
                    user.students.session_year_id=session_year
                    user.students.course_id=course_obj
                    user.students.gender=sex
                    user.students.profile_pic=profile_pic_url
                    user.save()
                    messages.success(request,"Successfully Added Student")
                    return HttpResponseRedirect(reverse("add_student"))
                except:
                    messages.error(request,"Failed to Add Student")
                    return HttpResponseRedirect(reverse("add_student"))
            else:
                form=AddStudentForm(request.POST)
                return render(request, "hod_template/add_student.html", {"form":form})

def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'hod_template/add_subject.html', {"courses":courses, "staffs":staffs})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_name = request.POST.get("subject")
        course_id = request.POST.get("Class")
        course = Courses.objects.get(id=course_id)
        staff_name = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_name)

        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))

def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, 'hod_template/manage_staff.html', {"staffs":staffs})

def manage_student(request):
    students = Students.objects.all()
    return render(request, 'hod_template/manage_student.html', {"students":students})

def manage_course(request):
    courses = Courses.objects.all()
    return render(request, 'hod_template/manage_course.html', {"courses":courses})

def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request, 'hod_template/manage_subject.html', {"subjects":subjects})

def edit_staff(request, staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff.html",{"staff":staff})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Edited Successfuly")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed To Edit")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id":staff_id}))

def edit_student(request, student_id):
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['course'].initial=student.course_id.id
    form.fields['sex'].initial=student.gender
    form.fields['session_year_id'].initial=student.session_year_id
    
    return render(request,"hod_template/edit_student.html",{"student":student, "form":form, "id":student_id, "username":student.admin.username})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id == None:
            return HttpResponseRedirect(reverse("manage_student"))
        
        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            email=form.cleaned_data["email"]
            username=form.cleaned_data["username"]
            address=form.cleaned_data["address"]
            session_year_id=form.cleaned_data["session_year_id"]
            course_id=form.cleaned_data["course"]
            sex=form.cleaned_data["sex"]

            if request.FILES.get('profile_pic', False):
                profile_pic=request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name,profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=student_id)

                user.first_name=first_name
                user.last_name=last_name
                user.email=email
                user.username=username
                user.save()

                student = Students.objects.get(admin=student_id)

                student.address=address
                session_year = SessionYearModel.objects.get(id=session_year_id)
                student.session_year_id=session_year
                student.gender=sex
                course=Courses.objects.get(id=course_id)
                student.course_id= course
                if profile_pic_url!=None:
                    student.profile_pic = profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request,"Edited Successfuly")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed To Edit")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id":student_id}))
        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin=student_id)
            return render(request, "hod_template/edit_student.html", {"student":student, "form":form, "id":student_id, "username":student.admin.username})

def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course.html", {"course":course})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course")

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request,"Edited Successfuly")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id":course_id}))
        except:
            messages.error(request,"Failed To Edit")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
        


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_subject.html",{"subject":subject, "staffs":staffs, "courses":courses})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject")
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id =staff
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            subject.save()
            messages.success(request,"Edited Successfuly")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed To Edit")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))

def manage_session(request):
    return render(request, 'hod_template/manage_session.html')
def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")
        session_term = request.POST.get("session_term")
        session_term_year = request.POST.get("session_term_year")
    try:
        sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year, session_term=session_term, session_year_session=session_term_year)
        sessionyear.save()
        student_obj=Students.objects.all()
        session_year = SessionYearModel.objects.get(id=sessionyear.id)
        for students in student_obj:
            students.session_year_id = session_year
            students.save()
        messages.success(request,"Added Successfuly")
        return HttpResponseRedirect(reverse("manage_session"))
    except:
        messages.error(request,"Failed To Add")
        return HttpResponseRedirect(reverse("manage_session"))

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def staff_feedback_message(request):
    feedbacks=FeedBackStaffs.objects.all()
    return render(request,"hod_template/staff_feedback.html",{"feedbacks":feedbacks})

def student_feedback_message(request):
    feedbacks=FeedBackStudent.objects.all()
    return render(request,"hod_template/student_feedback.html",{"feedbacks":feedbacks})

@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_leave_view(request):
    leaves=LeaveReportStaff.objects.all()
    return render(request,"hod_template/staff_leave_view.html",{"leaves":leaves})

def student_leave_view(request):
    leaves=LeaveReportStudent.objects.all()
    return render(request,"hod_template/student_leave_view.html",{"leaves":leaves})

def student_approve_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def student_disapprove_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_approve_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def staff_disapprove_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            # if password!=None and password!="":
            #     customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

def edit_session_year(request):
    session = SessionYearModel.objects.all()
    return render(request, "hod_template/edit_session_year.html", {"sessions":session})

def delete_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Sucessfully Deleted Session")
        return HttpResponseRedirect(reverse("edit_session_year"))
    except:
        messages.error(request, "Failed to Delete Session Year")
        return HttpResponseRedirect(reverse("edit_session_year"))

def delete_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    try:
        course.delete()
        messages.success(request, "Sucessfully Deleted Class")
        return HttpResponseRedirect(reverse("manage_course"))
    except:
        messages.error(request, "Failed to Delete Class")
        return HttpResponseRedirect(reverse("manage_course"))