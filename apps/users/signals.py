import os
from django.dispatch import receiver
from django.db.models.signals import (
    pre_delete,
    pre_save
)
from .models import User


def delete_user_picture(image):
    try:
        os.remove(image.path)
        print(f"{image.path} \033[92mremoved\033[0m.")
    except Exception as e:
        print(f"\033[91m{image.path} doesn't exist.\033[0m")
        # this is not good, we should handle the exception in a nice way
        pass


@receiver(pre_delete, sender=User)
def delete_picture_on_user_delete(instance, **kwargs):
    delete_user_picture(instance.image)


@receiver(pre_save, sender=User)
def delete_old_picture_on_user_update(instance, **kwargs):
    id = instance.id
    if (len(User.objects.filter(id=id))):
        old_image = User.objects.get(id=id).picture
        new_image = instance.picture
        if (old_image != new_image):
            delete_user_picture(old_image)
