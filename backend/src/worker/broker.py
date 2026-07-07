from src.config import settings
from taskiq_redis import ListQueueBroker

broker = ListQueueBroker(url=settings.redis_url)
