from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    def handle(self, *args, **options):
        '''
           Command to drop all groups and populate 4 defaults group in order to manage permissions for users
        '''
        print("Deleting existing groups...")
        Group.objects.all().delete()

        #groups = ['Administrators', 'Technicians', 'Managers', 'Sellers']
        groups = (('Administradores', '1'),
                   ('Técnicos', '2'),
                   ('Operadores', '3'),
                   ('Revisores', '4'),
                  )
        for group in groups:
            print("Creating {} group...".format(group))
            try:
                group_instance = Group.objects.create(id=group[1], name=group[0])
                group_instance.save()  # por si las moscas
                print("{} group created.".format(group))
            except AttributeError as error:
                print(f"Error creating grup: {error}")
        print("Finish!.")


