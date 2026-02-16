#!/usr/bin/env python
"""
Script pour créer automatiquement un superuser
"""
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'School_Management.settings')
django.setup()

User = get_user_model()

# Vérifier si admin existe déjà
if User.objects.filter(username='admin').exists():
    print("✅ L'administrateur 'admin' existe déjà")
else:
    # Créer le superuser
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@school.com',
        password='Admin@123456',
        user_type='admin',
        first_name='School',
        last_name='Admin'
    )
    print(f"✅ Superuser créé avec succès!")
    print(f"   Username: admin")
    print(f"   Password: Admin@123456")
    print(f"   Email: admin@school.com")
