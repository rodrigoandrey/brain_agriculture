import factory
from faker import Faker

from produtores.models import Produtor, Fazenda, Safra, Cultura
from validate_docbr import CPF, CNPJ

faker = Faker()
cpf = CPF()
cnpj = CNPJ()


class ProdutorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Produtor

    nome = factory.LazyAttribute(lambda _: faker.name())

    # Gerar aleatoriamente CPF ou CNPJ válido
    cpf = factory.LazyAttribute(lambda _: cpf.generate())
    cnpj = factory.LazyAttribute(lambda _: cnpj.generate())


class FazendaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Fazenda

    nome = factory.LazyAttribute(lambda _: faker.company())
    cidade = factory.LazyAttribute(lambda _: faker.city())
    estado = factory.LazyAttribute(lambda _: faker.state_abbr())
    area_total = factory.LazyAttribute(lambda _: faker.random_int(min=50, max=1000))
    area_agricultavel = factory.LazyAttribute(lambda o: o.area_total * faker.random.uniform(0.5, 0.9))
    area_vegetacao = factory.LazyAttribute(lambda o: o.area_total - o.area_agricultavel)
    produtor = factory.SubFactory(ProdutorFactory)  # Relacionado ao Produtor


class SafraFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Safra

    nome = factory.LazyAttribute(lambda _: f"Safra")
    ano = factory.LazyAttribute(lambda _: faker.year())
    fazenda = factory.SubFactory(FazendaFactory)  # Relacionado à Fazenda


class CulturaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cultura

    nome = factory.LazyAttribute(lambda _: faker.random_element(['Soja', 'Milho', 'Café', 'Algodão', 'Trigo']))
    fazenda = factory.SubFactory(FazendaFactory)  # Relacionado à Fazenda
    safra = factory.SubFactory(SafraFactory)  # Relacionado à Safra
