from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .forms import EstimateUploadForm
from .models import Estimate
from .serializers import EstimateSerializer
from .tasks import process_estimate_task


def test_cache_view(request):
    cache.set("my_key", "Привет, я из Redis!", 30)  # Хранить 30 секунд
    val = cache.get("my_key")
    print(val)  # Выведет в консоль
    return HttpResponse(f"Значение из кэша: {val}")

@login_required
@cache_page(5)  # Кэшировать на 5 секунд
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


class EstimateListCreateAPIView(generics.ListCreateAPIView):
    queryset = Estimate.objects.all().order_by('-created_at')
    serializer_class = EstimateSerializer
    permission_classes = [IsAuthenticated] 

    def perform_create(self, serializer):
        estimate = serializer.save()
        process_estimate_task.delay(estimate.id)
