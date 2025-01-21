
# Brain Agriculture

**Brain Agriculture** é uma aplicação Django que utiliza Docker para facilitar a execução em ambientes controlados. Ela gerencia o cadastro de produtores rurais, fazendas e safras, e fornece um dashboard com informações e gráficos.

## Instruções para execução

### Pré-requisitos

- **Docker** e **Docker Compose** versão 2.3 ou superior devem estar instalados no seu sistema.
  
### Configuração e Execução

1. Clone o repositório do projeto:
   ```bash
   https://github.com/rodrigoandrey/agriculture.git
   cd brain_agriculture
   ```

2. Certifique-se de que todos os requisitos do projeto estão listados no arquivo `requirements.txt`.

3. Para iniciar a aplicação, execute o seguinte comando:
   ```bash
   docker-compose up --build
   ```

   Isso irá:
   - Construir a imagem do Django
   - Configurar o PostgreSQL 16 como banco de dados
   - Executar as migrações necessárias automaticamente
   - Carregar os dados iniciais (fixtures)

   A aplicação estará disponível em `http://localhost:8000`.

### Executando Testes

A aplicação utiliza o framework de testes do Django. Para rodar os testes automatizados, utilize o seguinte comando:

```bash
docker-compose exec web python manage.py test
```

## Endpoints

### 1. Cadastro de Produtores Rurais - `/api/v1/produtores/`

Este endpoint gerencia o cadastro de produtores rurais e está disponível através de um viewset, com suporte a todos os métodos HTTP (GET, POST, PUT, DELETE).

#### Exemplo de requisição para criação de novo produtor:

**URL:** `/api/v1/produtores/`

**Método:** `POST`

**Corpo da requisição (JSON):**
```json
{
  "cpf": "71260178048",
  "cnpj": "38335003000159",
  "nome": "José da Silva",
  "fazendas": [
    {
      "nome": "Fazenda Esperança",
      "cidade": "Uberlândia",
      "estado": "MG",
      "area_total": 100.0,
      "area_agricultavel": 70.0,
      "area_vegetacao": 30.0,
      "safras": [
        {
          "ano": 2021,
          "culturas": [
            {
              "nome": "Soja"
            },
            {
              "nome": "Milho"
            }
          ]
        },
        {
          "ano": 2022,
          "culturas": [
            {
              "nome": "Café"
            }
          ]
        }
      ]
    }
  ]
}
```

### 2. Dashboard - `/api/dashboard/`

Este endpoint retorna informações agregadas sobre as fazendas e gráficos de uso. Ele é usado para renderizar dados do dashboard da aplicação.

**URL:** `/api/dashboard/`

**Método:** `GET`

**Exemplo de resposta (JSON):**
```json
{
  "total_fazendas": 32,
  "total_hectares": "15162.00",
  "grafico_estado_url": "http://localhost:8000/media/grafico_estado.png",
  "grafico_cultura_url": "http://localhost:8000/media/grafico_cultura.png",
  "grafico_uso_solo_url": "http://localhost:8000/media/grafico_uso_solo.png"
}
```

## Conclusão

Agora você tem o ambiente configurado e a aplicação pronta para ser utilizada. Para mais informações, consulte a documentação completa ou entre em contato com a equipe de desenvolvimento.
