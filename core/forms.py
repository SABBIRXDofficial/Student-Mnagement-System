from django import forms
from .models import Role, Permission, User, Login, Student, Course, Fee, Exam


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name', 'role_desc']
        widgets = {
            'role_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['per_role', 'per_name', 'per_module']
        widgets = {
            'per_role':   forms.Select(attrs={'class': 'form-select'}),
            'per_name':   forms.TextInput(attrs={'class': 'form-control'}),
            'per_module': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'user_mobile', 'user_email', 'user_address']
        widgets = {
            'user_name':    forms.TextInput(attrs={'class': 'form-control'}),
            'user_mobile':  forms.TextInput(attrs={'class': 'form-control'}),
            'user_email':   forms.EmailInput(attrs={'class': 'form-control'}),
            'user_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class LoginForm(forms.ModelForm):
    user_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Login
        fields = ['login_username', 'login_role', 'user', 'user_password']
        widgets = {
            'login_username': forms.TextInput(attrs={'class': 'form-control'}),
            'login_role':     forms.Select(attrs={'class': 'form-select'}),
            'user':           forms.Select(attrs={'class': 'form-select'}),
        }


class StudentForm(forms.ModelForm):
    stu_pass = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label='Password')

    class Meta:
        model = Student
        fields = ['stu_name', 'stu_mobile', 'stu_add', 'stu_email', 'stu_pass']
        widgets = {
            'stu_name':   forms.TextInput(attrs={'class': 'form-control'}),
            'stu_mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'stu_add':    forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'stu_email':  forms.EmailInput(attrs={'class': 'form-control'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['crs_name', 'crs_desc', 'crs_type', 'student']
        widgets = {
            'crs_name': forms.TextInput(attrs={'class': 'form-control'}),
            'crs_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'crs_type': forms.TextInput(attrs={'class': 'form-control'}),
            'student':  forms.Select(attrs={'class': 'form-select'}),
        }


class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['fee_desc', 'fee_type', 'course', 'fee_amt']
        widgets = {
            'fee_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fee_type': forms.TextInput(attrs={'class': 'form-control'}),
            'course':   forms.Select(attrs={'class': 'form-select'}),
            'fee_amt':  forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_desc', 'exam_type']
        widgets = {
            'exam_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'exam_type': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LoginAuthForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
