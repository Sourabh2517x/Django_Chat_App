from django.db import models
import uuid
from users.models import User
from model_utils.models import TimeStampedModel
from .utils import default_usage_end

class BaseIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    class Meta:
        abstract = True


class Conversation(TimeStampedModel, BaseIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title or f"Conversation {self.id}"


class Message(TimeStampedModel):

    class SenderChoices(models.TextChoices):
        USER = "user", "User"
        BOT = "bot", "Bot"

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.CharField(max_length=10, choices=SenderChoices.choices)
    content = models.TextField()

    def __str__(self):
        return f"{self.sender}: {self.content[:30]}"


class Plan(models.Model):

    class PlanChoices(models.TextChoices):
        FREE = "FREE", "Free"
        STANDARD = "STANDARD", "Standard"
        PRO = "PRO", "Pro"

    plan_name = models.CharField(
        max_length=10, choices=PlanChoices.choices, unique=True
    )
    plan_description = models.CharField(max_length=255)
    token_limit = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    features = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.plan_name

    @classmethod
    def get_free_plan(cls):
        return cls.objects.get(plan_name=cls.PlanChoices.FREE)


class PurchasePlan(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, default=Plan.get_free_plan)
    tokens_used = models.PositiveIntegerField(default=0)
    usage_end_date = models.DateTimeField(default=default_usage_end)

    def __str__(self):
        return f"{self.user.username} - {self.plan.plan_name}"
    
