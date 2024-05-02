from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from management.models import CustomUser, Staffs, StudentAssignments, Courses, Students, StudentResult, Subjects, SessionYearModel, FeedBackStudent, FeedBackStaffs
# Register your fmodels here.

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)
admin.site.register(Staffs)
admin.site.register(Courses)
admin.site.register(Students)
admin.site.register(Subjects)
admin.site.register(FeedBackStudent)
admin.site.register(FeedBackStaffs)
admin.site.register(SessionYearModel)
admin.site.register(StudentResult)
admin.site.register(StudentAssignments)