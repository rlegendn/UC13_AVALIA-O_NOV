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