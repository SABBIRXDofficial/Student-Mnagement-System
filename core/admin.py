from django.contrib import admin
from .models import Role, Permission, User, Login, Student, Course, Fee, Exam


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name', 'role_desc')
    search_fields = ('role_name',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('per_id', 'per_role', 'per_name', 'per_module')
    list_filter = ('per_role', 'per_module')
    search_fields = ('per_name', 'per_module')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'user_email', 'user_mobile')
    search_fields = ('user_name', 'user_email')


@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('login_id', 'login_username', 'login_role', 'user')
    list_filter = ('login_role',)
    search_fields = ('login_username',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('stu_id', 'stu_name', 'stu_email', 'stu_mobile')
    search_fields = ('stu_name', 'stu_email')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('crs_id', 'crs_name', 'crs_type', 'student')
    list_filter = ('crs_type',)
    search_fields = ('crs_name',)


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('fee_id', 'fee_type', 'course', 'fee_amt')
    list_filter = ('fee_type',)
    search_fields = ('fee_type',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_id', 'exam_type', 'exam_desc')
    search_fields = ('exam_type',)
