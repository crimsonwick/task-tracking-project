from django.core.management import BaseCommand

from TaskTrackingApp import settings
from api.users.models import AccessLevel, Role, User
from django.contrib.auth.models import Group, Permission


def add_roles():
    roles = AccessLevel.DICT
    for acl, role in roles.items():
        role_object = Role.objects.filter(name=role, access_level=acl)
        created = Group.objects.get_or_create(name=role)

        if role_object.exists():
            print(f'Role {role} exists')
            continue
        else:
            r = Role(name=role, access_level=acl)
            r.save()
            print(f'Role {role} newly added.')
    print('All above roles have been added/updated successfully.')

    for email in settings.SUPER_ADMIN:
        print(email)
        object = {}
        object['first_name'] = 'super'
        object['last_name'] = 'admin'
        object['email'] = email
        object['is_staff'] = True
        object['is_approved'] = True
        object['is_active'] = True
        object['is_superuser'] = True
        object['role'] = Role.objects.get(code__exact=AccessLevel.CEO_CODE)
        try:
            user = User.objects.create(**object)
            user.set_password("Pass1234@")
            user.save()
            print(user.role)
            print("Super User Created Successfully")
        except Exception as e:
            if hasattr(e.__cause__, 'pgcode') and e.__cause__.pgcode == '23505':
                print("Super User already exists")
            print(str(e))

class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            add_roles()
        except Exception as e:
            print(e)