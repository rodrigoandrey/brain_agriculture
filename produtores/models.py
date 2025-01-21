import logging

from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.models import BaseModelMixin
from produtores.validators import validate_cpf, validate_cnpj

logger_error = logging.getLogger('django.errors')


class Produtor(BaseModelMixin):
    nome = models.CharField('Nome completo', max_length=255, null=False, blank=False,
                            help_text='Nome completo')
    cpf = models.CharField('CPF', max_length=11, unique=True, null=True, blank=True,
                           help_text='Apenas números sem pontos ou traços', validators=[validate_cpf])
    cnpj = models.CharField('CNPJ', max_length=14, unique=True, null=True, blank=True,
                            help_text='Apenas números sem pontos ou traços', validators=[validate_cnpj])

    class Meta:
        verbose_name = 'Produtor'
        verbose_name_plural = 'Produtores'

    def __str__(self):
        return f'{self.nome}'


class Fazenda(BaseModelMixin):
    produtor = models.ForeignKey(Produtor, on_delete=models.SET_NULL, related_name='fazendas', verbose_name='Produtor',
                                 null=True, blank=True)
    nome = models.CharField('Nome da fazenda', max_length=255, null=False, blank=False)
    cidade = models.CharField('Cidade', max_length=128, null=False, blank=False)
    estado = models.CharField('Estado', max_length=2, null=False, blank=False,
                              help_text='Sigla do Estado (2 caractéres | Ex. SP, RJ)')
    area_total = models.DecimalField('Área total', max_digits=10, decimal_places=2, null=True, blank=True,
                                     help_text='Área total em hectares', default=0)
    area_agricultavel = models.DecimalField('Área agricultável', max_digits=10, decimal_places=2, null=True, blank=True,
                                            help_text='Área agricultável em hectares', default=0)
    area_vegetacao = models.DecimalField('Área de vegetação', max_digits=10, decimal_places=2, null=True, blank=True,
                                         help_text='Área de vegetação em hectares', default=0)

    def clean(self):
        if (self.area_agricultavel + self.area_vegetacao) > self.area_total:  # NOQA
            raise ValidationError('A soma das áreas agricultável e vegetação não pode exceder a área total.')

    def __str__(self):
        return f'{self.nome}'


class Safra(BaseModelMixin):
    nome = models.CharField('Safra', max_length=128, null=False, blank=False, default='Safra')
    ano = models.IntegerField('Ano', null=False, blank=False, help_text='Ano da safra')
    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE, related_name='safras', verbose_name='Fazenda',
                                null=False, blank=False)

    def __str__(self):
        return f'{self.nome} {self.ano}'


class Cultura(BaseModelMixin):
    nome = models.CharField('Nome cultura', max_length=255, null=False, blank=False,
                            help_text='Nome da cultura plantada')
    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE, related_name='culturas', verbose_name='Fazenda',
                                null=False, blank=False)
    safra = models.ForeignKey(Safra, on_delete=models.SET_NULL, related_name='culturas', verbose_name='Safra',
                              null=True, blank=True)

    def __str__(self):
        return f'{self.nome}'
