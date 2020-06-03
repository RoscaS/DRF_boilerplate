import os
from django.dispatch import receiver
from django.db.models.signals import (
    pre_delete,
    pre_save,
    post_save,
)
from .models import (
    Category,
    Article,
)

def delete_image(image):
    try:
        os.remove(image.path)
    except:
        print(f"\033[91m{image.path} doesn't exist.\033[0m")
        return

    print(f"{image.path} \033[92mremoved\033[0m.")

@receiver(pre_delete, sender=Article)
def delete_image_on_article_delete(instance, **kwargs):
    delete_image(instance.image)

@receiver(pre_save, sender=Article)
def delete_old_image_on_article_update(instance, **kwargs):
    id = instance.id
    if (len(Article.objects.filter(id=id))):
        old_image = Article.objects.get(id=id).image
        new_image = instance.image
        if (old_image != new_image):
            delete_image(old_image)

@receiver(post_save, sender=Category)
def set_category_weight(instance, **kwargs):
    if kwargs['created']:
        instance.weight = Category.objects.count()
        instance.save()

@receiver(post_save, sender=Article)
def set_article_weight(instance, **kwargs):
    if kwargs['created']:
        instance.weight = instance.category.articles.count()
        instance.save()
