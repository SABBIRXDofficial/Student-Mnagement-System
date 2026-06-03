from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Count, Sum

from .models import Role, Permission, User, Login, Student, Course, Fee, Exam
from .forms import (RoleForm, PermissionForm, UserForm, LoginForm,
                    StudentForm, CourseForm, FeeForm, ExamForm)


# ────────────────────────────────────────────────
# DECORATOR
# ────────────────────────────────────────────────
def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ────────────────────────────────────────────────
# HOME (public landing page)
# ────────────────────────────────────────────────
def home_view(request):
    return render(request, 'home.html')


# ────────────────────────────────────────────────
# AUTH
# ────────────────────────────────────────────────
def login_view(request):
    if request.session.get('user_id'):
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        try:
            lo = Login.objects.select_related('user', 'login_role').get(login_username=username)
            if check_password(password, lo.user_password):
                request.session['user_id']  = lo.user.user_id
                request.session['username'] = lo.login_username
                request.session['role']     = lo.login_role.role_name
                messages.success(request, f'Welcome, {lo.user.user_name}!')
                return redirect('dashboard')
            messages.error(request, 'Incorrect password.')
        except Login.DoesNotExist:
            messages.error(request, 'Username not found.')
    return render(request, 'core/login.html')


def logout_view(request):
    request.session.flush()
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        name   = request.POST.get('user_name', '').strip()
        email  = request.POST.get('user_email', '').strip()
        mobile = request.POST.get('user_mobile', '').strip()
        pwd    = request.POST.get('password', '').strip()
        if not (name and email and pwd):
            messages.error(request, 'Name, email and password are required.')
            return render(request, 'core/register.html')
        if User.objects.filter(user_email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'core/register.html')
        user = User.objects.create(user_name=name, user_email=email, user_mobile=mobile)
        role, _ = Role.objects.get_or_create(
            role_name='Student', defaults={'role_desc': 'Default student role'}
        )
        Login.objects.create(
            login_username=email,
            user_password=make_password(pwd),
            login_role=role,
            user=user
        )
        messages.success(request, 'Account created! You can now log in.')
        return redirect('login')
    return render(request, 'core/register.html')


# ────────────────────────────────────────────────
# DASHBOARD
# ────────────────────────────────────────────────
@login_required_custom
def dashboard(request):
    total_students = Student.objects.count()
    total_courses  = Course.objects.count()
    total_exams    = Exam.objects.count()
    total_users    = User.objects.count()
    total_roles    = Role.objects.count()
    total_fees     = Fee.objects.aggregate(t=Sum('fee_amt'))['t'] or 0
    total_max      = max(total_students, total_courses, total_exams, total_users, total_roles, 1)
    ctx = {
        'total_students':  total_students,
        'total_courses':   total_courses,
        'total_exams':     total_exams,
        'total_users':     total_users,
        'total_roles':     total_roles,
        'total_fees':      total_fees,
        'total_max':       total_max,
        'recent_students': Student.objects.order_by('-stu_id')[:5],
        'recent_courses':  Course.objects.select_related('student').order_by('-crs_id')[:5],
        'recent_fees':     Fee.objects.select_related('course').order_by('-fee_id')[:5],
        'recent_exams':    Exam.objects.order_by('-exam_id')[:5],
        'active':          'dashboard',
    }
    return render(request, 'core/dashboard.html', ctx)


# ────────────────────────────────────────────────
# STUDENT
# ────────────────────────────────────────────────
@login_required_custom
def student_list(request):
    if request.method == 'POST':
        name  = request.POST.get('stu_name', '').strip()
        email = request.POST.get('stu_email', '').strip()
        mob   = request.POST.get('stu_mobile', '').strip()
        add   = request.POST.get('stu_add', '').strip()
        pwd   = request.POST.get('stu_pass', '').strip()
        if name and email and pwd:
            if Student.objects.filter(stu_email=email).exists():
                messages.error(request, f'Email {email} already exists.')
            else:
                Student.objects.create(stu_name=name, stu_email=email,
                                       stu_mobile=mob, stu_add=add,
                                       stu_pass=make_password(pwd))
                messages.success(request, f'Student "{name}" added.')
        else:
            messages.error(request, 'Name, email and password are required.')
        return redirect('student_list')
    students = Student.objects.order_by('-stu_id')
    return render(request, 'core/student_list.html', {'students': students, 'active': 'students'})

@login_required_custom
def student_create(request): return redirect('student_list')

@login_required_custom
def student_edit(request, pk):
    obj = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save(); messages.success(request, 'Student updated.')
        return redirect('student_list')
    return render(request, 'core/form.html',
                  {'form': form, 'title': f'Edit Student — {obj.stu_name}',
                   'back_url': 'student_list', 'active': 'students'})

@login_required_custom
def student_delete(request, pk):
    obj = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        obj.delete(); messages.success(request, 'Student deleted.')
        return redirect('student_list')
    return render(request, 'core/confirm_delete.html',
                  {'obj': obj, 'title': 'Delete Student',
                   'back_url': 'student_list', 'active': 'students'})


# ────────────────────────────────────────────────
# COURSE
# ────────────────────────────────────────────────
@login_required_custom
def course_list(request):
    if request.method == 'POST':
        name   = (request.POST.get('crs_name_full','') or request.POST.get('crs_name','')).strip()
        c_type = request.POST.get('crs_type','').strip()
        desc   = request.POST.get('crs_desc','').strip()
        stu_id = request.POST.get('crs_stu_id','').strip()
        student = None
        if stu_id:
            try: student = Student.objects.get(pk=int(stu_id))
            except: messages.error(request, f'Student ID {stu_id} not found.'); return redirect('course_list')
        if name:
            Course.objects.create(crs_name=name, crs_type=c_type, crs_desc=desc, student=student)
            messages.success(request, f'Course "{name}" added.')
        else:
            messages.error(request, 'Course name is required.')
        return redirect('course_list')
    courses = Course.objects.select_related('student').order_by('-crs_id')
    return render(request, 'core/course_list.html', {'courses': courses, 'active': 'courses'})

@login_required_custom
def course_create(request): return redirect('course_list')

@login_required_custom
def course_edit(request, pk):
    obj = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save(); messages.success(request, 'Course updated.')
        return redirect('course_list')
    return render(request, 'core/form.html',
                  {'form': form, 'title': f'Edit Course — {obj.crs_name}',
                   'back_url': 'course_list', 'active': 'courses'})

@login_required_custom
def course_delete(request, pk):
    obj = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        obj.delete(); messages.success(request, 'Course deleted.')
        return redirect('course_list')
    return render(request, 'core/confirm_delete.html',
                  {'obj': obj, 'title': 'Delete Course',
                   'back_url': 'course_list', 'active': 'courses'})


# ────────────────────────────────────────────────
# FEE
# ────────────────────────────────────────────────
@login_required_custom
def fee_list(request):
    if request.method == 'POST':
        crs_id   = request.POST.get('fee_crs_id','').strip()
        fee_type = request.POST.get('fee_type','').strip()
        fee_amt  = request.POST.get('fee_amt','0').strip()
        fee_desc = request.POST.get('fee_desc','').strip()
        try:
            course = Course.objects.get(pk=int(crs_id))
            Fee.objects.create(course=course, fee_type=fee_type,
                               fee_amt=float(fee_amt), fee_desc=fee_desc)
            messages.success(request, 'Fee record added.')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect('fee_list')
    fees = Fee.objects.select_related('course').order_by('-fee_id')
    return render(request, 'core/fee_list.html', {'fees': fees, 'active': 'fees'})

@login_required_custom
def fee_create(request): return redirect('fee_list')

@login_required_custom
def fee_edit(request, pk):
    obj = get_object_or_404(Fee, pk=pk)
    form = FeeForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save(); messages.success(request, 'Fee updated.')
        return redirect('fee_list')
    return render(request, 'core/form.html',
                  {'form': form, 'title': 'Edit Fee Record',
                   'back_url': 'fee_list', 'active': 'fees'})

@login_required_custom
def fee_delete(request, pk):
    obj = get_object_or_404(Fee, pk=pk)
    if request.method == 'POST':
        obj.delete(); messages.success(request, 'Fee deleted.')
        return redirect('fee_list')
    return render(request, 'core/confirm_delete.html',
                  {'obj': obj, 'title': 'Delete Fee',
                   'back_url': 'fee_list', 'active': 'fees'})


# ────────────────────────────────────────────────
# EXAM
# ────────────────────────────────────────────────
@login_required_custom
def exam_list(request):
    if request.method == 'POST':
        exam_type = request.POST.get('exam_type','').strip()
        exam_desc = request.POST.get('exam_desc','').strip()
        if exam_type:
            Exam.objects.create(exam_type=exam_type, exam_desc=exam_desc)
            messages.success(request, f'Exam "{exam_type}" added.')
        else:
            messages.error(request, 'Exam type required.')
        return redirect('exam_list')
    exams = Exam.objects.annotate(student_count=Count('students')).order_by('-exam_id')
    return render(request, 'core/exam_list.html', {'exams': exams, 'active': 'exams'})

@login_required_custom
def exam_create(request): return redirect('exam_list')

@login_required_custom
def exam_edit(request, pk):
    obj = get_object_or_404(Exam, pk=pk)
    form = ExamForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save(); messages.success(request, 'Exam updated.')
        return redirect('exam_list')
    return render(request, 'core/form.html',
                  {'form': form, 'title': 'Edit Exam',
                   'back_url': 'exam_list', 'active': 'exams'})

@login_required_custom
def exam_delete(request, pk):
    obj = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        obj.delete(); messages.success(request, 'Exam deleted.')
        return redirect('exam_list')
    return render(request, 'core/confirm_delete.html',
                  {'obj': obj, 'title': 'Delete Exam',
                   'back_url': 'exam_list', 'active': 'exams'})


# ────────────────────────────────────────────────
# USER
# ────────────────────────────────────────────────
@login_required_custom
def user_list(request):
    if request.method == 'POST':
        name   = request.POST.get('user_name','').strip()
        email  = request.POST.get('user_email','').strip()
        mobile = request.POST.get('user_mobile','').strip()
        addr   = request.POST.get('user_address','').strip()
        if name and email:
            if User.objects.filter(user_email=email).exists():
                messages.error(request, f'Email {email} already in use.')
            else:
                User.objects.create(user_name=name, user_email=email,
                                    user_mobile=mobile, user_address=addr)
                messages.success(request, f'User "{name}" added.')
        else:
            messages.error(request, 'Name and email are required.')
        return redirect('user_list')
    users = User.objects.order_by('-user_id')
    return render(request, 'core/user_list.html', {'users': users, 'active': 'users'})

@login_required_custom
def user_create(request): return redirect('user_list')

@login_required_custom
def user_edit(request, pk):
    obj = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save(); messages.success(request, 'User updated.')
        return redirect('user_list')
    return render(request, 'core/form.html',
                  {'form': form, 'title': f'Edit User — {obj.user_name}',
                   'back_url': 'user_list', 'active': 'users'})

@login_required_custom
def user_delete(request, pk):
    obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        obj.delete(); messages.success(request, 'User deleted.')
        return redirect('user_list')
    return render(request, 'core/confirm_delete.html',
                  {'obj': obj, 'title': 'Delete User',
                   'back_url': 'user_list', 'active': 'users'})


# ────────────────────────────────────────────────
# ROLE
# ────────────────────────────────────────────────
@login_required_custom
def role_list(request):
    if request.method == 'POST':
        name = request.POST.get('role_name','').strip()
        desc = request.POST.get('role_desc','').strip()
        if name:
            Role.objects.create(role_name=name, role_desc=desc)
            messages.success(request, f'Role "{name}" added.')
        else:
            messages.error(request, 'Role name required.')
        return redirect('role_list')
    roles = Role.objects.annotate(user_count=Count('users')).order_by('role_id')
    return render(request, 'core/role_list.html', {'roles': roles, 'active': 'roles'})

@login_required_custom
def role_create(request): return redirect('role_list')

@login_required_custom
def role_edit(request, pk):
    obj = get_object_or_404(Role, pk=pk)
    form = RoleForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save(); messages.success(request, 'Role updated.')
        return redirect('role_list')
    return render(request, 'core/form.html',
                  {'form': form, 'title': f'Edit Role — {obj.role_name}',
                   'back_url': 'role_list', 'active': 'roles'})

@login_required_custom
def role_delete(request, pk):
    obj = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        obj.delete(); messages.success(request, 'Role deleted.')
        return redirect('role_list')
    return render(request, 'core/confirm_delete.html',
                  {'obj': obj, 'title': 'Delete Role',
                   'back_url': 'role_list', 'active': 'roles'})


# ────────────────────────────────────────────────
# PERMISSION
# ────────────────────────────────────────────────
@login_required_custom
def permission_list(request):
    if request.method == 'POST':
        role_id = request.POST.get('per_role','').strip()
        p_name  = request.POST.get('per_name','').strip()
        p_mod   = request.POST.get('per_module','').strip()
        try:
            role = Role.objects.get(pk=int(role_id))
            Permission.objects.create(per_role=role, per_name=p_name, per_module=p_mod)
            messages.success(request, 'Permission added.')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect('permission_list')
    roles = Role.objects.all()
    perms = Permission.objects.select_related('per_role').order_by('per_id')
    return render(request, 'core/permission_list.html',
                  {'perms': perms, 'roles': roles, 'active': 'permissions'})

@login_required_custom
def permission_create(request): return redirect('permission_list')

@login_required_custom
def permission_edit(request, pk):
    obj = get_object_or_404(Permission, pk=pk)
    form = PermissionForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save(); messages.success(request, 'Permission updated.')
        return redirect('permission_list')
    return render(request, 'core/form.html',
                  {'form': form, 'title': 'Edit Permission',
                   'back_url': 'permission_list', 'active': 'permissions'})

@login_required_custom
def permission_delete(request, pk):
    obj = get_object_or_404(Permission, pk=pk)
    if request.method == 'POST':
        obj.delete(); messages.success(request, 'Permission deleted.')
        return redirect('permission_list')
    return render(request, 'core/confirm_delete.html',
                  {'obj': obj, 'title': 'Delete Permission',
                   'back_url': 'permission_list', 'active': 'permissions'})


# ────────────────────────────────────────────────
# LOGIN RECORDS
# ────────────────────────────────────────────────
@login_required_custom
def login_list(request):
    if request.method == 'POST':
        username = request.POST.get('login_username','').strip()
        role_id  = request.POST.get('login_role','').strip()
        user_id  = request.POST.get('user','').strip()
        pwd      = request.POST.get('user_password','').strip()
        try:
            role = Role.objects.get(pk=int(role_id))
            user = User.objects.get(pk=int(user_id))
            Login.objects.create(login_username=username, login_role=role,
                                 user=user, user_password=make_password(pwd))
            messages.success(request, f'Login for "{username}" created.')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect('login_list')
    roles  = Role.objects.all()
    users  = User.objects.all()
    logins = Login.objects.select_related('user','login_role').order_by('-login_id')
    return render(request, 'core/login_list.html',
                  {'logins': logins, 'roles': roles, 'users': users, 'active': 'logins'})

@login_required_custom
def login_create(request): return redirect('login_list')

@login_required_custom
def login_edit(request, pk):
    obj = get_object_or_404(Login, pk=pk)
    form = LoginForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save(); messages.success(request, 'Login updated.')
        return redirect('login_list')
    return render(request, 'core/form.html',
                  {'form': form, 'title': f'Edit Login — {obj.login_username}',
                   'back_url': 'login_list', 'active': 'logins'})

@login_required_custom
def login_delete(request, pk):
    obj = get_object_or_404(Login, pk=pk)
    if request.method == 'POST':
        obj.delete(); messages.success(request, 'Login deleted.')
        return redirect('login_list')
    return render(request, 'core/confirm_delete.html',
                  {'obj': obj, 'title': 'Delete Login Record',
                   'back_url': 'login_list', 'active': 'logins'})
