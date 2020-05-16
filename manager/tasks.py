import logging

from asana_client.celery import app

logger = logging.getLogger(__name__)


@app.task(name='Test me')
def test_task():
    logger.info("HELLO")

