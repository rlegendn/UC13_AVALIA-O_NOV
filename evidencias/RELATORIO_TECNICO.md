# Relatório técnico de manutenção

**Estudante:**  
**Data:** 25/11/2026

## Estado inicial e diagnóstico
Descreva os problemas observados com as evidências que fundamentaram a investigação.

## Intervenções
Explique as causas identificadas e as modificações realizadas.

## Validação
Apresente testes realizados, resultados esperados e obtidos e como verificou a persistência.

## Entrega e versionamento
Informe o repositório próprio, os commits realizados e eventuais limitações.

me ajude a continuar o meu relatorio.md, seguindo minha forma de falar sem mudar oque ja fiz da atividade anterior
# Correção da API

## Primeiro problema

A API apresentava um erro de conexão com o banco, tendo em vista que o seu nome estava conflitante, o banco existente se chamava  eventos.db, enquanto o chamado na comunicação se chamava  eventos_novos.db, essa diferença de nomes fazia com que o get tentasse buscar informações em um banco não existente, devido a isso a API sempre retornava erro de servidor, apos corrigir na linha 8 do codigo o problema alteramos apenas o nome do arquivo do banco  para o seu  nome correto, apos isso o banco passou a devolver  a resposta corretamente, o get puxava shows existentes no banco.

## Segundo problema

### Cenario

Um dos 3 items do banco DB não é mostrado ao executar a busca do GET /api/eventos/{evento_id},o codigo deveria retornar 200 se id fosse existente ou 404 caso o ida não existisse entretanto alguns ids mesmo existindo não aparencem, muito provavel que exista uma restrição fechando o acesso(causa possivel e não obrigatoria).

### Solução

 Para que todos os ids sejam localizados, apaguei da função  listar eventos  a linha onde estava escrito WHERE capacidade>=50, essa restrição inpedia que todas as capcidades fossem mostradas.

 ## Terceiro Problema

 ### Cenario 

o codigo do bloco da função cadastrar eventos, contido na linha
29 do codigo ate a linha 33 apresenta resposta diferente ao que estava acontecendo na API, tendo em base que essa função esta criando um novo dado, a resposta http precisa ser "201, CREATED", equanto ela retornava "200, OK".

### Solução

A unica mudança foi trocar a resposta (status_code=status.HTTP_201_OK) por (status_code=status.HTTP_201_CREATED) que o sistema passou a responder o erro corretamente.

## Quarto Problema

### Cenario

Nas linhas 35 q 42 do arquivo main estava aplicado o bloco da função de comprar ingressos, o problema evidenciado é que a a API não retorna a resposta correta quando o usuario tentava comprar uma quantidade invalida de ingressos, ambas as outras respostas eram devidamente retornadas como(200,404 e 422) porem 409 não.

### Primeira Tentativa

Ao executar a primeira tentativa de correção, utilizei um metodo por logica considerei que PedidoIngressos guardava a quantidade de ingressos a serem comprados e atulizados supostamente guardaria a quantidade de ingressos existente no banco, mas acredito que ouve um equivoco considerando que o erro retornado na API é o erro 500, que é erro interno do servidor.

##### Codigo do Teste

if PedidoIngressos > atualizado:
        raise HTTPException(status_code=409, detail="Evento não encontrado")

### Segunda Tentativa

Analisando o banco de dados, era necessario criar uma validação dentro da função registrar_ingressos(), foi percebido que o banco não fazia a validação necessaria para voltar erro 409, então foi mudando a arquitetura do codigo, neste momento o banco faz uma comparaçãoentre capacidade e ingressos_comprados, ao ingressos serem maiores que capacidade, da erro 409 por conta que não podem ser comprados mais ingressos do que existem no banco.

Na função comprar_ngresso nas linha 35 do codigo "main.py", colocamos  condicional para avaliar se a varaiavel atualisado é valida ou não , se a quantidade exceder o valor  ele apresenta erro 409 e "Vagas Insuficientes"

## Quinto Problema

### Cenario

Ao verificar a função de consulta de disponibilidade de ingressos, foi percebido que o calculo das vagas restantes estava incorreto. A função consultava a capacidade total do evento e os ingressos vendidos, entretanto, o calculo estava somando os dois valores em vez de subtrair. Dessa forma, a API retornava um número incorreto de vagas disponíveis.

### Solução

Foi alterada a lógica do calculo dentro da função consultar_disponibilidade(), no arquivo repositorio.py. A operação passou a subtrair os ingressos vendidos da capacidade total do evento, fazendo com que a API retornasse corretamente a quantidade de vagas restantes. Também foi adicionada a verificação para que, caso o evento não exista, seja retornado o erro 404.

## Sexto Problema

### Cenario

Na função listar_mais_vendidos(), responsável por retornar os eventos que possuem maior quantidade de ingressos vendidos, a ordenação estava incorreta. O banco estava organizando os eventos em ordem crescente, fazendo com que os eventos com menos vendas fossem apresentados primeiro, contrariando o objetivo da função.

### Solução

Foi alterada a ordenação da consulta SQL dentro da função listar_mais_vendidos(), trocando a ordenação de ASC para DESC na coluna ingressos_vendidos. Dessa forma, os eventos passaram a ser apresentados do maior número de ingressos vendidos para o menor, mantendo também a organização pelo ID caso existisse empate. A consulta continuou limitada a três eventos.

## Sétimo Problema

### Cenario

Na função de cancelamento de ingressos, foi identificado que o sistema não possuía uma validação adequada para impedir que fossem cancelados mais ingressos do que haviam sido vendidos. Isso poderia fazer com que a quantidade de ingressos vendidos no banco de dados ficasse negativa, prejudicando as informações armazenadas.

### Solução

Foi adicionada uma validação dentro da função cancelar_ingressos(), no arquivo repositorio.py, fazendo com que o banco verifique se a quantidade de ingressos vendidos é suficiente para realizar o cancelamento solicitado. Caso a quantidade solicitada seja maior do que a existente, a operação não é realizada.

Também foi adicionada uma validação na função responsável pelo cancelamento, no arquivo main.py, para verificar se o evento existe e se a quantidade solicitada é válida. Caso o evento não exista, o sistema retorna 404, caso a quantidade seja inválida retorna 422 e, caso não existam ingressos suficientes para o cancelamento, retorna 409.

## Oitavo Problema

### Cenario

A API não possuía uma função responsável por atualizar os dados de um evento existente, sendo necessário implementar uma nova rota PUT /api/eventos/{evento_id}. A função deveria permitir a alteração do nome e da capacidade do evento, entretanto, a capacidade não poderia ser alterada para um valor menor do que a quantidade de ingressos já vendidos.

### Solução

Foi criada a função atualizar_evento() dentro do arquivo repositorio.py, responsável por atualizar os dados do evento no banco SQLite. Também foi criada a rota PUT no arquivo main.py, que recebe os novos dados do evento e realiza as validações necessárias.

Caso o evento não exista, a API retorna 404. Caso a nova capacidade seja menor do que a quantidade de ingressos vendidos, a API retorna 409, impedindo que a alteração prejudique os ingressos já comercializados. Caso os dados enviados sejam inválidos, o sistema retorna 422. Com os dados válidos, o evento é atualizado e a API retorna 200.

## Nono Problema

### Cenario

A API não possuía uma rota responsável por apresentar um relatório geral de ocupação dos eventos cadastrados. Era necessário obter a quantidade total de eventos, a capacidade total, o número de ingressos vendidos e a quantidade de vagas disponíveis, utilizando os dados existentes no banco de dados.

### Solução

Foi criada a função relatorio_ocupacao() dentro do arquivo repositorio.py, utilizando uma consulta SQL para calcular os valores necessários diretamente no banco de dados. A consulta passou a retornar o total de eventos, a capacidade total, os ingressos vendidos e as vagas disponíveis.

Também foi criada a rota GET /api/relatorios/ocupacao no arquivo main.py, responsável por disponibilizar os dados calculados. Dessa forma, o sistema passou a apresentar um relatório geral de ocupação dos eventos cadastrados.

## Décimo Problema

### Cenario

A API não possuía uma função que permitisse a exclusão controlada de eventos. Era necessário implementar a rota DELETE /api/eventos/{evento_id}, entretanto, a exclusão não poderia acontecer caso o evento já possuísse ingressos vendidos, evitando a perda de informações relacionadas às vendas realizadas.

### Solução

Foi criada a função excluir_evento() dentro do arquivo repositorio.py, responsável por verificar se o evento existe e se possui ingressos vendidos antes de realizar a exclusão. Também foi implementada a rota DELETE no arquivo main.py, responsável por executar a operação e retornar os status HTTP adequados.

Caso o evento não exista, a API retorna 404. Caso existam ingressos vendidos, a exclusão é impedida e o sistema retorna 409. Caso a exclusão seja realizada com sucesso, a API retorna 204, indicando que o evento foi excluído sem retornar conteúdo na resposta.

evidencias testes
![alt text](<Captura de tela 2026-11-27 111502.png>) ![alt text](<Captura de tela 2026-11-27 111437.png>) ![alt text](<Captura de tela 2026-11-27 111424.png>) ![alt text](<Captura de tela 2026-11-27 111403.png>) ![alt text](<Captura de tela 2026-11-27 111337.png>) ![alt text](<Captura de tela 2026-11-27 111314.png>) ![alt text](<Captura de tela 2026-11-27 111242.png>) ![alt text](<Captura de tela 2026-11-27 111204.png>) ![alt text](<Captura de tela 2026-11-27 111145.png>) ![alt text](<Captura de tela 2026-11-27 111136.png>) ![alt text](<Captura de tela 2026-11-27 110904.png>) ![alt text](<Captura de tela 2026-11-27 110847.png>) ![alt text](<Captura de tela 2026-11-27 110825.png>) ![alt text](<Captura de tela 2026-11-27 110816.png>) ![alt text](<Captura de tela 2026-11-27 110751.png>) ![alt text](<Captura de tela 2026-11-27 110739.png>) ![alt text](<Captura de tela 2026-11-27 110652.png>) ![alt text](<Captura de tela 2026-11-27 110628.png>)![
    
](<Captura de tela 2026-11-27 110611.png>) ![
    
](<Captura de tela 2026-11-27 110559.png>) ![
    
](<Captura de tela 2026-11-11 163339.png>) ![
    
](<Captura de tela 2026-11-11 163330.png>)