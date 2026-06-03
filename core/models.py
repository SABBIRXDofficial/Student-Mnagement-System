from django.db import models
from django.contrib.auth.hashers import make_password


# ─────────────────────────────────────────────
# ROLES
# ─────────────────────────────────────────────
class Role(models.Model):
    role_id   = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)
    role_desc = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.role_name


# ─────────────────────────────────────────────
# PERMISSION
# ─────────────────────────────────────────────
class Permission(models.Model):
    per_id     = models.AutoField(primary_key=True)
    per_role   = models.ForeignKey(Role, on_delete=models.CASCADE,
                                   db_column='per_role_id', related_name='permissions')
    per_name   = models.CharField(max_length=100)
    per_module = models.CharField(max_length=100)

    class Meta:
        db_table = 'permission'

    def __str__(self):
        return f"{self.per_name} ({self.per_module})"


# ─────────────────────────────────────────────
# USER
# ─────────────────────────────────────────────
class User(models.Model):
    user_id      = models.AutoField(primary_key=True)
    user_name    = models.CharField(max_length=150)
    user_mobile  = models.CharField(max_length=20, blank=True, null=True)
    user_email   = models.EmailField(unique=True)
    user_address = models.TextField(blank=True, null=True)
    # Many-to-many: User Has Roles
    roles        = models.ManyToManyField(Role, through='UserHasRole',
                                          related_name='users')

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.user_name


# ─────────────────────────────────────────────
# USER HAS ROLE (junction)
# ─────────────────────────────────────────────
class UserHasRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role_id')

    class Meta:
        db_table = 'user_has_roles'
        unique_together = ('user', 'role')


# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
class Login(models.Model):
    login_id       = models.AutoField(primary_key=True)
    login_role     = models.ForeignKey(Role, on_delete=models.RESTRICT,
                                       db_column='login_role_id')
    login_username = models.CharField(max_length=150, unique=True)
    user_password  = models.CharField(max_length=255)
    user           = models.ForeignKey(User, on_delete=models.CASCADE,
                                       db_column='user_id', related_name='logins')

    class Meta:
        db_table = 'login'

    def save(self, *args, **kwargs):
        # Hash password if not already hashed
        if self.user_password and not self.user_password.startswith('pbkdf2_'):
            self.user_password = make_password(self.user_password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.login_username


# ─────────────────────────────────────────────
# STUDENT
# ─────────────────────────────────────────────
class Student(models.Model):
    stu_id     = models.AutoField(primary_key=True)
    stu_name   = models.CharField(max_length=150)
    stu_mobile = models.CharField(max_length=20, blank=True, null=True)
    stu_add    = models.TextField(blank=True, null=True)
    stu_email  = models.EmailField(unique=True)
    stu_pass   = models.CharField(max_length=255)
    # Manage: users who manage this student
    managers   = models.ManyToManyField(User, through='UserManagesStudent',
                                        related_name='managed_students')

    class Meta:
        db_table = 'student'

    def save(self, *args, **kwargs):
        if self.stu_pass and not self.stu_pass.startswith('pbkdf2_'):
            self.stu_pass = make_password(self.stu_pass)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.stu_name


# ─────────────────────────────────────────────
# USER MANAGES STUDENT (junction)
# ─────────────────────────────────────────────
class UserManagesStudent(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='stu_id')

    class Meta:
        db_table = 'user_manages_student'
        unique_together = ('user', 'student')


# ─────────────────────────────────────────────
# COURSE
# ─────────────────────────────────────────────
class Course(models.Model):
    crs_id  = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                db_column='crs_stu_id', related_name='courses')
    crs_name = models.CharField(max_length=200)
    crs_desc = models.TextField(blank=True, null=True)
    crs_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'course'

    def __str__(self):
        return self.crs_name


# ─────────────────────────────────────────────
# FEES
# ─────────────────────────────────────────────
class Fee(models.Model):
    fee_id  = models.AutoField(primary_key=True)
    fee_desc = models.TextField(blank=True, null=True)
    fee_type = models.CharField(max_length=100)
    course   = models.ForeignKey(Course, on_delete=models.RESTRICT,
                                 db_column='fee_crs_id', related_name='fees')
    fee_amt  = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'fees'

    def __str__(self):
        return f"{self.fee_type} - {self.fee_amt}"


# ─────────────────────────────────────────────
# EXAM
# ─────────────────────────────────────────────
class Exam(models.Model):
    exam_id   = models.AutoField(primary_key=True)
    exam_desc = models.TextField(blank=True, null=True)
    exam_type = models.CharField(max_length=100)
    # Has: students who have this exam
    students  = models.ManyToManyField(Student, through='StudentHasExam',
                                       related_name='exams')

    class Meta:
        db_table = 'exam'

    def __str__(self):
        return f"{self.exam_type} (ID: {self.exam_id})"


# ─────────────────────────────────────────────
# STUDENT HAS EXAM (junction)
# ─────────────────────────────────────────────
class StudentHasExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='stu_id')
    exam    = models.ForeignKey(Exam, on_delete=models.CASCADE, db_column='exam_id')

    class Meta:
        db_table = 'student_has_exam'
        unique_together = ('student', 'exam')
