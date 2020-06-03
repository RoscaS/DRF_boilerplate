from django.db import models


class Example(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Examples'

    def __str__(self):
        return self.name

