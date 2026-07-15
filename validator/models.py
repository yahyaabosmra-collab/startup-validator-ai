from django.db import models

from django.conf import settings
class StartupIdea(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="startups",
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=255)
    idea = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class ValidationReport(models.Model):
    startup = models.ForeignKey(
        StartupIdea,
        on_delete=models.CASCADE,
        related_name="reports",
    )

    business_analysis = models.JSONField()
    market_analysis = models.JSONField()
    risk_analysis = models.JSONField()

    final_report = models.JSONField()
    score = models.FloatField(
    null=True,
    blank=True,
)

    final_verdict = models.CharField(
    max_length=50,
    null=True,
    blank=True,
)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # def __str__(self):
    #     return f"Validation Report - {self.startup.title}"
    


class RevokedRefreshToken(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="revoked_refresh_tokens",
    )

    jti = models.CharField(
        max_length=255,
        unique=True,
    )

    expires_at = models.DateTimeField()

    revoked_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.user.username} - {self.jti}"