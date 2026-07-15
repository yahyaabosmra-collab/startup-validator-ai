from django.urls import path

from validator.views import dashboard_view, login_view, me_view, register_view,report_detail_view, validate_startup_view,reports_list_view,refresh_token_view,  logout_view


urlpatterns = [
    path(
        "validate-startup/",
        validate_startup_view,
        name="validate_startup",
    ),
    path(
        "reports/<int:report_id>/",
        report_detail_view,
        name="report_detail",
    ),
    path(
        "reports/",
        reports_list_view,
        name="reports_list",
    ),
    path(
        "auth/login/",
        login_view,
        name="login",
    ),
    path(
        "dashboard/",
        dashboard_view,
        name="dashboard",
    ),      
    path(
        "auth/me/",
        me_view,
        name="me",
    ),
      path(
        "auth/register/",
        register_view,
        name="register",
    ),
    path(
    "auth/refresh/",
    refresh_token_view,
    name="token-refresh",
),

path(
    "auth/logout/",
    logout_view,
    name="logout",
),
]