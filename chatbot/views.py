from django.shortcuts import render, get_object_or_404
from .services import GeminiService, GeminiServiceError
from .models import Conversation, Message, Plan, PurchasePlan
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import reset_tokens


class ChatView(LoginRequiredMixin, View):

    def post(self, request):
        user_input = request.POST.get("message")
        conversation_id = request.POST.get("conversation_id")

        subscription, _ = PurchasePlan.objects.get_or_create(user=request.user)
        reset_tokens(subscription)

        if subscription.tokens_used >= subscription.plan.token_limit:
            return JsonResponse(
                {
                    "error": "Token limit exceeded",
                    "tokens_used": subscription.tokens_used,
                },
                status=403,
            )

        if conversation_id:
            conversation = get_object_or_404(
                Conversation, id=conversation_id, user=request.user
            )
            is_new = False
        else:
            conversation = Conversation.objects.create(
                user=request.user, title=user_input[:35]
            )
            is_new = True

        gemini_service = GeminiService()

        try:
            bot_response, tokens_used = gemini_service.generate_response(
                conversation, user_input
            )
        except GeminiServiceError as exc:
            return JsonResponse(
                {
                    "error": exc.message,
                    "conversation_id": conversation.id,
                    "conversation_title": conversation.title,
                },
                status=exc.status_code,
            )

        Message.objects.create(
            conversation=conversation, sender="user", content=user_input
        )

        Message.objects.create(
            conversation=conversation, sender="bot", content=bot_response
        )

        subscription.tokens_used += tokens_used
        subscription.save(update_fields=["tokens_used"])

        return JsonResponse(
            {
                "user_message": user_input,
                "bot_response": bot_response,
                "conversation_id": conversation.id,
                "conversation_title": conversation.title,
                "is_new": is_new,
                "tokens_used": subscription.tokens_used,
            }
        )

    def get(self, request):
        conversation_id = request.GET.get("conversation_id")

        subscription, _ = PurchasePlan.objects.get_or_create(user=request.user)
        reset_tokens(subscription)

        conversations = Conversation.objects.filter(user=request.user).order_by(
            "-created"
        )

        if conversation_id:
            conversation = get_object_or_404(
                Conversation, id=conversation_id, user=request.user
            )
            messages = conversation.messages.order_by("created")
        else:
            conversation = ""
            messages = []

        return render(
            request,
            "chatbot/chat.html",
            {
                "messages": messages,
                "conversation_id": conversation.id if conversation else conversation,
                "conversations": conversations,
                "subscription": subscription,
            },
        )


class PlanView(TemplateView):
    template_name = "chatbot/plan.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plans"] = Plan.objects.all().order_by("price")

        user = self.request.user
        context["current_plan"] = getattr(
            getattr(user, "purchaseplan", None), "plan", None
        )

        return context
