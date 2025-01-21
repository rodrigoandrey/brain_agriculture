import logging

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from validate_docbr import CPF, CNPJ

logger_general = logging.getLogger('general')


def validate_cpf(value):
    cpf_validator = CPF()
    if not cpf_validator.validate(value):
        logger_general.info("O CPF informado %s não é valido" % value)
        raise ValidationError(
            _("O CPF informado %(value)s não é valido"),
            params={"value": value},
        )


def validate_cnpj(value):
    cnpj_validator = CNPJ()
    if not cnpj_validator.validate(value):
        logger_general.info("O CNPJ informado %s não é valido" % value)
        raise ValidationError(
            _("O CNPJ informado %(value)s não é valido"),
            params={"value": value},
        )
