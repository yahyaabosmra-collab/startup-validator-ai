from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse


User = get_user_model()


def generate_access_token(user):
    now = datetime.now(timezone.utc)

    payload = {
        "user_id": user.id,
        "username": user.get_username(),
        "type": "access",
        "iat": now,
        "exp": now + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_MINUTES
        ),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

def generate_refresh_token(user):
    now = datetime.now(timezone.utc)

    payload = {
        "user_id": user.id,
        "username": user.get_username(),
        "type": "refresh",
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + timedelta(
            days=settings.JWT_REFRESH_TOKEN_DAYS
        ),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return JsonResponse(
                {
                    "error": "Authentication credentials were not provided."
                },
                status=401,
            )

        token = auth_header.split(" ", 1)[1].strip()

        if not token:
            return JsonResponse(
                {"error": "Invalid token."},
                status=401,
            )

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )

            if payload.get("type") != "access":
                return JsonResponse(
                    {"error": "Invalid token type."},
                    status=401,
                )

            user = User.objects.get(
                id=payload["user_id"],
                is_active=True,
            )

        except jwt.ExpiredSignatureError:
            return JsonResponse(
                {"error": "Token has expired."},
                status=401,
            )

        except jwt.InvalidTokenError:
            return JsonResponse(
                {"error": "Invalid token."},
                status=401,
            )

        except (User.DoesNotExist, KeyError):
            return JsonResponse(
                {"error": "User not found."},
                status=401,
            )

        request.user = user

        return view_func(request, *args, **kwargs)

    return wrapper