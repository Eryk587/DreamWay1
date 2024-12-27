import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_registration(client):
    response = client.post(reverse('register'), {
        'username': 'testuser',
        'password1': 'strongpassword123',
        'password2': 'strongpassword123',
    })
    assert response.status_code == 302  # Redirect to login
    assert User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_user_login(client, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='password123')
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'password123',
    })
    assert response.status_code == 302  # Redirect after login
