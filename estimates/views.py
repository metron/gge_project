from django.shortcuts import redirect, render

from .forms import EstimateUploadForm
from .models import Estimate
from .services import process_new_estimate
from .tasks import process_estimate_task


def index(request):
    if request.method == 'POST':
        # Если прислали данные — наполняем форму
        form = EstimateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            estimate = form.save()  # Магия ModelForm: сохраняет запись в БД!
            # process_new_estimate(estimate)

            # ОТПРАВЛЯЕМ В ФОН
            # .delay() передает аргумент в RabbitMQ, и воркер его подхватит
            process_estimate_task.delay(estimate.id)

            return redirect('index') # Перезагружаем страницу после успеха
    else:
        # Если просто открыли страницу — даем пустую форму
        form = EstimateUploadForm()

    context = {
        'form': form,
        'estimates': Estimate.objects.all().order_by('-created_at'),
    }

    return render(request, 'estimates/upload.html', context)

