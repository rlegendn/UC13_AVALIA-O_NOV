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

# correção da API

## primeiro problema

A API apresentava um erro de conexão com o banco, tendo em vista que o seu nome estava conflitante, o banco existente se chamava  eventos.db, enquanto o chamado na comunicação se chamava  eventos_novos.db, essa diferença de nomes fazia com que o get tentasse buscar informações em um banco não existente, devido a isso a API sempre retornava erro de servidor, apos corrigir na linha 8 do codigo o problema alteramos apenas o nome do arquivo do banco  para o seu  nome correto, apos isso o banco passou a devolver  a resposta corretamente, o get puxava shows existentes no banco.

## segundo problema

### cenario

um dos 3 items do banco DB não é mostrado ao executar a busca do GET /api/eventos/{evento_id},o codigo deveria retornar 200 se id fosse existente ou 404 caso o ida não existisse entretanto alguns ids mesmo existindo não aparencem, muito provavel que exista uma restrição fechando o acesso(causa possivel e não obrigatoria).

### solução

 para que todos os ids sejam localizados, apaguei da função  listar eventos  a linha onde estava escrito WHERE capacidade>=50, essa restrição inpedia que todas as capcidades fossem mostradas.

 ## terceiro problema

 ### cenario 

 o codigo do bloco da função cadastrar eventos, contido na linha
29 do codigo ate a linha 33 apresenta resposta diferente ao que estava acontecendo na API, tendo em base que essa função esta criando um novo dado, a resposta http precisa ser "201, CREATED", equanto ela retornava "200, OK".

### solução

a unica mudança foi trocar a resposta (status_code=status.HTTP_201_OK) por (status_code=status.HTTP_201_CREATED) que o sistema passou a responder o erro corretamente.
