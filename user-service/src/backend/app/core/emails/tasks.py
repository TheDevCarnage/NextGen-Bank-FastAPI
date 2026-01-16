import asyncio
from backend.app.core.celery_app import celery_app
from fastapi_mail import MessageSchema, MessageType, MultipartSubtypeEnum
from backend.app.core.logging import get_logger
from backend.app.core.emails.config import fastmail

logger = get_logger(__name__)


@celery_app.task(
    name="send_email_task",
    bind=True,
    max_retries=3,
    soft_time_limit=60,
    auto_retry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=60,
)
def send_email_task(
    self, *, recipients: list[str], subject: str, html_content: str, plain_content: str
) -> bool:
    """
    Celery task to send an email asynchronously.

    Args:
        recipients (list[str]): List of recipient email addresses.
        subject (str): Subject of the email.
        html_content (str): HTML content of the email.
        plain_content (str | None): Plain text content of the email. Optional.
    """
    try:
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=html_content,
            subtype=MessageType.html,
            alternative_body=plain_content,
            multipart_subtype=MultipartSubtypeEnum.alternative,
        )

        asyncio.run(fastmail.send_message(message))
        logger.info(f"Email sent to {recipients} with subject '{subject}'")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipients}: {str(e)}")
        return False
