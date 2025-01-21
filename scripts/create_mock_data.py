from factories import ProdutorFactory, FazendaFactory, SafraFactory, CulturaFactory


def run():
    # Cria 10 produtores, cada um com 1 a 3 fazendas, 1 a 3 safras e 1 a 3 culturas por safra
    for _ in range(10):
        produtor = ProdutorFactory()
        fazendas = FazendaFactory.create_batch(3, produtor=produtor)
        for fazenda in fazendas:
            safras = SafraFactory.create_batch(3, fazenda=fazenda)
            for safra in safras:
                CulturaFactory.create_batch(3, fazenda=fazenda, safra=safra)

    print("Dados mockados criados com sucesso!")
