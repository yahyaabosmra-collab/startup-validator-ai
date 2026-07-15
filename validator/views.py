import json
import jwt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from validator.services.validation_service import ValidationService
from validator.models import ValidationReport , StartupIdea, RevokedRefreshToken
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from .auth_utils import generate_access_token, jwt_required,generate_refresh_token
from django.db.models import Avg
from datetime import datetime, timezone

User = get_user_model()
@csrf_exempt
def register_view(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed."},
            status=405,
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON body."},
            status=400,
        )

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")

    if not username or not email or not password:
        return JsonResponse(
            {
                "error": "username, email and password are required."
            },
            status=400,
        )

    if password != confirm_password:
        return JsonResponse(
            {"error": "Passwords do not match."},
            status=400,
        )

    if len(password) < 8:
        return JsonResponse(
            {
                "error": "Password must be at least 8 characters."
            },
            status=400,
        )

    if User.objects.filter(
        username__iexact=username
    ).exists():
        return JsonResponse(
            {"error": "Username already exists."},
            status=400,
        )

    if User.objects.filter(
        email__iexact=email
    ).exists():
        return JsonResponse(
            {"error": "Email already exists."},
            status=400,
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    return JsonResponse(
        {
            "message": "User registered successfully.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
        },
        status=201,
    )



@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed."},
            status=405,
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON body."},
            status=400,
        )

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return JsonResponse(
            {
                "error": "username and password are required."
            },
            status=400,
        )

    user = authenticate(
        request,
        username=username,
        password=password,
    )

    if user is None:
        return JsonResponse(
            {"error": "Invalid username or password."},
            status=401,
        )

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    return JsonResponse(
        {
            "message": "Login successful.",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
        },
        status=200,
    )

@csrf_exempt
def refresh_token_view(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "error": "Method not allowed."
            },
            status=405,
        )

    try:
        data = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "error": "Invalid JSON body."
            },
            status=400,
        )

    refresh_token = data.get(
        "refresh_token",
        "",
    ).strip()

    if not refresh_token:
        return JsonResponse(
            {
                "error": "refresh_token is required."
            },
            status=400,
        )

    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        if payload.get("type") != "refresh":
            return JsonResponse(
                {
                    "error": "Invalid token type."
                },
                status=401,
            )

        jti = payload.get("jti")

        if not jti:
            return JsonResponse(
                {
                    "error": "Invalid refresh token."
                },
                status=401,
            )

        if RevokedRefreshToken.objects.filter(
            jti=jti
        ).exists():
            return JsonResponse(
                {
                    "error": "Refresh token has been revoked."
                },
                status=401,
            )

        user = User.objects.get(
            id=payload["user_id"],
            is_active=True,
        )

    except jwt.ExpiredSignatureError:
        return JsonResponse(
            {
                "error": "Refresh token has expired."
            },
            status=401,
        )

    except jwt.InvalidTokenError:
        return JsonResponse(
            {
                "error": "Invalid refresh token."
            },
            status=401,
        )

    except (
        User.DoesNotExist,
        KeyError,
    ):
        return JsonResponse(
            {
                "error": "User not found."
            },
            status=401,
        )

    new_access_token = generate_access_token(user)

    return JsonResponse(
        {
            "access_token": new_access_token
        },
        status=200,
    )


@jwt_required
def me_view(request):
    return JsonResponse(
        {
            "user": {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            }
        },
        status=200,
    )
@csrf_exempt
@jwt_required
def validate_startup_view(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "error": "Only POST requests are allowed."
            },
            status=405,
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "error": "Invalid JSON body."
            },
            status=400,
        )

    title = data.get("title", "").strip()
    idea = data.get("idea", "").strip()

    if not title or not idea:
        return JsonResponse(
            {
                "error": "title and idea are required."
            },
            status=400,
        )

    try:
        service = ValidationService()

        report = service.validate_startup(
        user=request.user,
        title=title,
        idea=idea,
        )

    except Exception as exc:
        return JsonResponse(
            {
                "error": "Startup analysis failed.",
                "details": str(exc),
            },
            status=500,
        )

    return JsonResponse(
        {
            "startup_id": report.startup.id,
            "report_id": report.id,
            "title": report.startup.title,
            "idea": report.startup.idea,
            "business_analysis": report.business_analysis,
            "market_analysis": report.market_analysis,
            "risk_analysis": report.risk_analysis,
            "final_score": float(report.score),
            "final_report": report.final_report,
        },
        status=201,
    )

@jwt_required
def report_detail_view(request, report_id):
    if request.method != "GET":
        return JsonResponse(
            {
                "error": "Only GET requests are allowed."
            },
            status=405,
        )

    try:
        report = ValidationReport.objects.select_related(
            "startup"
        ).get(id=report_id,startup__user=request.user,)

    except ValidationReport.DoesNotExist:
        return JsonResponse(
            {
                "error": "report not found."
            },
            status=404,
        )

    return JsonResponse(
        {
            "startup_id": report.startup.id,
            "report_id": report.id,
            "title": report.startup.title,
            "idea": report.startup.idea,
            "business_analysis": report.business_analysis,
            "market_analysis": report.market_analysis,
            "risk_analysis": report.risk_analysis,
            "final_score": float(report.score),
            "final_verdict": report.final_verdict,
            "final_report": report.final_report,
            "created_at": report.created_at.isoformat(),
            
        },
        status=200,
    )

@jwt_required
def reports_list_view(request):
    if request.method != "GET":
        return JsonResponse(
            {
                "error": "Only GET requests are allowed."
            },
            status=405,
        )

    reports = ValidationReport.objects.select_related(
        "startup"
    ).filter(
        startup__user=request.user
    ).order_by("-created_at")

    reports_data = []

    for report in reports:
        reports_data.append(
            {
                "startup_id": report.startup.id,
                "report_id": report.id,
                "title": report.startup.title,
                "final_score": float(report.score),
                "created_at": report.created_at.isoformat(),
            }
        )

    return JsonResponse(
        {
            "reports": reports_data
        },
        status=200,
    )


@jwt_required
def dashboard_view(request):
    if request.method != "GET":
        return JsonResponse(
            {
                "error": "Only GET requests are allowed."
            },
            status=405,
        )

    reports = ValidationReport.objects.select_related(
        "startup"
    ).filter(
        startup__user=request.user
    )

    total_reports = reports.count()

    total_startups = StartupIdea.objects.filter(
        user=request.user
    ).count()

    average_score = reports.aggregate(
        average=Avg("score")
    )["average"]

    recent_reports = reports.order_by(
        "-created_at"
    )[:5]

    recent_reports_data = []

    for report in recent_reports:
        recent_reports_data.append(
            {
                "report_id": report.id,
                "startup_id": report.startup.id,
                "title": report.startup.title,
                "final_score": float(report.score),
                "created_at": report.created_at.isoformat(),
            }
        )

    return JsonResponse(
        {
            "total_startups": total_startups,
            "total_reports": total_reports,
            "average_score": (
                round(float(average_score), 2)
                if average_score is not None
                else 0
            ),
            "recent_reports": recent_reports_data,
        },
        status=200,
    )



@csrf_exempt
def logout_view(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "error": "Method not allowed."
            },
            status=405,
        )

    try:
        data = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "error": "Invalid JSON body."
            },
            status=400,
        )

    refresh_token = data.get(
        "refresh_token",
        "",
    ).strip()

    if not refresh_token:
        return JsonResponse(
            {
                "error": "refresh_token is required."
            },
            status=400,
        )

    try:
        payload = jwt.decode(
            refresh_token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        if payload.get("type") != "refresh":
            return JsonResponse(
                {
                    "error": "Invalid token type."
                },
                status=401,
            )

        jti = payload.get("jti")

        if not jti:
            return JsonResponse(
                {
                    "error": "Invalid refresh token."
                },
                status=401,
            )

        user = User.objects.get(
            id=payload["user_id"],
            is_active=True,
        )

        expires_at = datetime.fromtimestamp(
            payload["exp"],
            tz=timezone.utc,
        )

    except jwt.ExpiredSignatureError:
        return JsonResponse(
            {
                "error": "Refresh token has expired."
            },
            status=401,
        )

    except jwt.InvalidTokenError:
        return JsonResponse(
            {
                "error": "Invalid refresh token."
            },
            status=401,
        )

    except (
        User.DoesNotExist,
        KeyError,
        ValueError,
    ):
        return JsonResponse(
            {
                "error": "Invalid refresh token."
            },
            status=401,
        )

    RevokedRefreshToken.objects.get_or_create(
        jti=jti,
        defaults={
            "user": user,
            "expires_at": expires_at,
        },
    )

    return JsonResponse(
        {
            "message": "Logout successful."
        },
        status=200,
    )