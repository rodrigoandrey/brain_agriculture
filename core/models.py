from django.db import models


class BaseModelManagerMixin(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()


class BaseModelMixin(models.Model):
    """Metodo|Mixin Base para controle de tempo e bit ativo no banco de dados"""
    created_at = models.DateTimeField('Criado em?', auto_now=False, auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Atualizado em?', auto_now=True, null=True)
    active_bit = models.BooleanField('Bit ativo?', default=True)

    class Meta:
        abstract = True

    objects = BaseModelManagerMixin()

BASE_MODEL_MIXIN_FIELDS = [f.name for f in BaseModelMixin._meta.fields]  # NOQA
