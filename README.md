# API de eventos

Aplicação para cadastro, consulta de eventos e venda de ingressos.

**Tecnologias:** Python, FastAPI e SQLite.

Projeto recebido para avaliação e manutenção na UC-13 — Técnico em Informática.

## Ambiente e execução
A completar pelo responsável pela manutenção.

## Operações e exemplos de uso
A completar pelo responsável pela manutenção.

## Verificação e manutenção
A completar com os resultados dos testes e as alterações realizadas.

# API de Eventos

## Como utilizar a API

Para utilizar a API, primeiro é necessario iniciar o servidor pelo terminal, utilizando o comando de execução do FastAPI(py -m uvicorn "app.main:app" --reload). Após o servidor estar ativo, a API pode ser acessada pela rota http://127.0.0.1:8000, que é a porta local utilizada para a comunicação com o sistema.

Para facilitar a utilização e os testes, o FastAPI disponibiliza uma documentação interativa através da rota http://127.0.0.1:8000/docs. Nela é possível visualizar todas as funções disponíveis na API, realizar requisições e observar as respostas retornadas pelo sistema.

Na função GET `/api/eventos`, é possível consultar todos os eventos cadastrados no banco de dados, enquanto a função GET `/api/eventos/{evento_id}` permite buscar um evento específico utilizando seu ID. Caso seja necessário cadastrar um novo evento, a função POST `/api/eventos` permite inserir informações como nome e capacidade, gerando um novo registro no banco.

Para realizar a compra de ingressos, é utilizada a função POST `/api/eventos/{evento_id}/ingressos`, onde é necessário informar a quantidade de ingressos desejada. O sistema verifica se a quantidade solicitada está dentro da capacidade disponível do evento, impedindo que sejam realizadas vendas acima do limite permitido.

A função GET `/api/eventos/{evento_id}/disponibilidade` permite consultar a quantidade de vagas restantes para determinado evento, considerando a capacidade total e os ingressos já vendidos. Já a função GET `/api/relatorios/mais-vendidos` apresenta os eventos com maior quantidade de ingressos vendidos, permitindo visualizar quais eventos possuem maior procura.

Também é possível realizar cancelamentos através da função POST `/api/eventos/{evento_id}/cancelamentos`, informando a quantidade de ingressos que deseja cancelar. A função PUT `/api/eventos/{evento_id}` permite alterar informações de um evento existente, como nome e capacidade, respeitando as validações aplicadas pelo sistema.

Por fim, a função GET `/api/relatorios/ocupacao` apresenta informações gerais sobre os eventos cadastrados, incluindo a capacidade total, quantidade de ingressos vendidos e vagas disponíveis. A função DELETE `/api/eventos/{evento_id}` permite excluir um evento, porém essa exclusão só é permitida quando não existem ingressos vendidos para ele.