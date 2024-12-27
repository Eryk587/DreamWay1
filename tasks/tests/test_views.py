import pytest
from django.urls import reverse
from tasks.models import Task, Category

@pytest.mark.django_db
def test_task_detail_view(client, django_user_model):
    # Tworzenie użytkownika
    user = django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    # Tworzenie kategorii i zadania
    category = Category.objects.create(name='Praca')
    task = Task.objects.create(
        title='Zadanie testowe',
        description='Opis testowego zadania',
        status='todo',
        due_date='2025-01-01',
        category=category,
        user=user
    )

    # Sprawdzanie szczegółów zadania
    response = client.get(reverse('task_detail', args=[task.pk]))
    assert response.status_code == 200
    assert 'Zadanie testowe' in response.content.decode()
    assert 'Opis testowego zadania' in response.content.decode()
    assert 'Praca' in response.content.decode()
