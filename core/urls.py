from django.urls import path
from . import views

urlpatterns = [
    # ── Public (homepage served by Django) ──
    path('',         views.home_view,     name='home'),
    path('login/',   views.login_view,    name='login'),
    path('logout/',  views.logout_view,   name='logout'),
    path('register/',views.register_view, name='register'),

    # ── SMS App ──
    path('dashboard/',  views.dashboard, name='dashboard'),

    path('students/',                 views.student_list,   name='student_list'),
    path('students/<int:pk>/edit/',   views.student_edit,   name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/add/',             views.student_create, name='student_create'),

    path('courses/',                  views.course_list,   name='course_list'),
    path('courses/<int:pk>/edit/',    views.course_edit,   name='course_edit'),
    path('courses/<int:pk>/delete/',  views.course_delete, name='course_delete'),
    path('courses/add/',              views.course_create, name='course_create'),

    path('fees/',                     views.fee_list,   name='fee_list'),
    path('fees/<int:pk>/edit/',       views.fee_edit,   name='fee_edit'),
    path('fees/<int:pk>/delete/',     views.fee_delete, name='fee_delete'),
    path('fees/add/',                 views.fee_create, name='fee_create'),

    path('exams/',                    views.exam_list,   name='exam_list'),
    path('exams/<int:pk>/edit/',      views.exam_edit,   name='exam_edit'),
    path('exams/<int:pk>/delete/',    views.exam_delete, name='exam_delete'),
    path('exams/add/',                views.exam_create, name='exam_create'),

    path('users/',                    views.user_list,   name='user_list'),
    path('users/<int:pk>/edit/',      views.user_edit,   name='user_edit'),
    path('users/<int:pk>/delete/',    views.user_delete, name='user_delete'),
    path('users/add/',                views.user_create, name='user_create'),

    path('roles/',                    views.role_list,   name='role_list'),
    path('roles/<int:pk>/edit/',      views.role_edit,   name='role_edit'),
    path('roles/<int:pk>/delete/',    views.role_delete, name='role_delete'),
    path('roles/add/',                views.role_create, name='role_create'),

    path('permissions/',                   views.permission_list,   name='permission_list'),
    path('permissions/<int:pk>/edit/',     views.permission_edit,   name='permission_edit'),
    path('permissions/<int:pk>/delete/',   views.permission_delete, name='permission_delete'),
    path('permissions/add/',               views.permission_create, name='permission_create'),

    path('logins/',                   views.login_list,   name='login_list'),
    path('logins/<int:pk>/edit/',     views.login_edit,   name='login_edit'),
    path('logins/<int:pk>/delete/',   views.login_delete, name='login_delete'),
    path('logins/add/',               views.login_create, name='login_create'),
]
