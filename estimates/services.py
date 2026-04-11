import time
from .models import Estimate

def process_new_estimate(estimate: Estimate):
    # 1. Сразу ставим статус "В обработке"
    estimate.status = 'processing'
    estimate.save()
    
    # 2. Здесь в будущем будет вызов парсера .gge
    # А пока просто имитируем задержку/работу
    print(f"Начинаем анализ файла: {estimate.file.name}")
    time.sleep(1)
    
    # 3. Допустим, проверка прошла успешно
    estimate.status = 'checked'
    estimate.save()
