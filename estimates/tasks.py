import time
from celery import shared_task
from .models import Estimate


@shared_task
def process_estimate_task(estimate_id):
    # Эта функция выполнится в отдельном процессе воркера!
    estimate = Estimate.objects.get(id=estimate_id)
    estimate.status = 'processing'
    estimate.save()
    
    time.sleep(10)  # Имитируем тяжелый парсинг GGE
    
    estimate.status = 'checked'
    estimate.save()
    return f"Estimate {estimate_id} processed"
