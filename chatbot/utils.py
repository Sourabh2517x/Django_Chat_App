from django.utils import timezone
from datetime import timedelta
import nh3, markdown


def reset_tokens(subscription):
    now = timezone.now()

    if now >= subscription.usage_end_date:
        delta = now - subscription.usage_end_date

        cycles = (delta.days // 7) + 1

        subscription.usage_end_date += timedelta(days=7 * cycles)
        subscription.tokens_used = 0
        subscription.save(update_fields=["tokens_used", "usage_end_date"])


def default_usage_end():
    return timezone.now() + timedelta(days=7)


def parse_response(response):
    text_parts = []

    for candidate in getattr(response, "candidates", []) or []:
        for part in getattr(getattr(candidate, "content", None), "parts", []) or []:
            text_parts.append(getattr(part, "text", ""))

    raw_text = "".join(text_parts).strip()

    usage = getattr(response, "usage_metadata", None)
    tokens = getattr(usage, "total_token_count", 0)

    formatted = markdown.markdown(
        raw_text,
        extensions=["fenced_code", "codehilite", "tables"],
    )

    clean_html = nh3.clean(
        formatted,
        tags={"p", "strong", "em", "code", "pre", "ul", "li", "ol", "a"},
        attributes={"a": {"href"}},
    )

    return clean_html, tokens
