# gerenciamento_estacionamento

A API permite o registro da entrada e saída de veículos, garantindo que a saída só aconteça após o pagamento, e calcula o valor do estacionamento baseado no tempo que o veículo permaneceu no local, também inclui um relatório das movimentações que aconteceram no estacionamento.

## TESTES

Rodar os testes apartir dos seguintes comandos:

- python manage.py test users.tests.test_user;
- python manage.py test users.tests.test_login;
- python manage.py test users.tests.test_entrada;
- python manage.py test users.tests.test_valor;
- python manage.py test users.tests.test_pagar;
- python manage.py test users.tests.test_saida;
- python manage.py test users.tests.test_relatorio;

Evita erros no teste por conta de conexão com banco de dados.

## Requisitos

- Python 3.x
- Django
- Django REST Framework
- PyJWT

## Configuração

1. Clone o repositório:
   ```bash
   git clone https://github.com/JUorlando/gerenciamento_estacionamento.git
