# If a documented django-task option is NOT configured in settings, use these values.
from django.conf import settings

hash = {
    "task_ALLOW_FILE_ATTACHMENTS": True,
    "task_COMMENT_CLASSES": [],
    "task_DEFAULT_ASSIGNEE": None,
    "task_LIMIT_FILE_ATTACHMENTS": [".jpg", ".gif", ".png", ".csv", ".pdf", ".zip"],
    "task_MAXIMUM_ATTACHMENT_SIZE": 5000000,
    "task_PUBLIC_SUBMIT_REDIRECT": "/",
    "task_STAFF_ONLY": True,
}

# These intentionally have no defaults (user MUST set a value if their features are used):
# task_DEFAULT_LIST_SLUG
# task_MAIL_BACKENDS
# task_MAIL_TRACKERS


def defaults(key: str):
    """Try to get a setting from project settings.
    If empty or doesn't exist, fall back to a value from defaults hash."""

    if hasattr(settings, key):
        val = getattr(settings, key)
    else:
        val = hash.get(key)
    return val
