# Changelog

Todas as mudanças notáveis neste projeto estarão listadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Versionamento semântico](https://semver.org/spec/v2.0.0.html).

## [Não publicado]

Segue abaixo funcionalidades para serem feitas ou ainda não publicadas.

### ADICIONADO

- Tipos de conteúdo
  - Documento
  - Imagem
  - Coleção: conjunto curado de notícias arquivadas e/ou documentos
  - Veículo da notícia

- Processos de auditoria
  - Faça um relatório da captura da notícia em PDF
  - Faça um perfil de Auditor

- Captura automática
  - Todas as capturas devem ser instâncias de documentos
  - Formatos:
    - HTML
    - Imagem

- Perfis de acesso para usuários
  - Adicionar os perfis visitante, membro, garimpador, moderador, editor e auditor (mais informações no arquivo de
  requisitos)

- Interface administrativa
  - Notícia Arquivada: Ícones para indicar a presença de capturas, ao invés de descrição textual do status
  - [OK] Notícia Arquivada: Link para a notícia no título
  - [OK] Notícia Arquivada: fazer uma classe para fazer um método comum de salvamento sobre os modelos do tipo `TraceableModel`
    - [OK] Esse método deve definir os usuários dos campos `created_by` e `modified_by`
  - Notícia Arquivada: desativar sinais e agendar jobs diretamente da interface administrativa no método `save_model`

- Busca de conteúdos
  - Faça uma busca multi-facetada
  - Utilize o ElasticSearch
  - Páginas
    - Busca com interface simples, estilo Google
    - Link para página de busca avançada, com critérios
    - Resultados
      - Filtros para limitar os resultados de acordo com critérios

- Páginas básicas
  - Inicial
  - Sobre
  - Contato
- Páginas individuais
  - Notícia arquivada
  - Documento
  - Imagem
  - Coleção

### MODIFICADO

- Workflow
  - Considere deixar para a fila de processamento apenas a captura de página
    - Ao menos o processamento básico seria feito sincronicamente
      - Ao menos o título da notícia seria populado sincronicamente
  - Se o servidor do redis estiver offline, os processamentos deverão ser executados sincronicamente

- Interface administrativa
  - Notícia Arquivada
    - Não salvar as flags no modelo, usá-las apenas no controller (formulário)
    - O campo de palavras-chave no formulário de inserção/edição da Notícia Arquivada deve permitir a digitação direta das
      palavras-chave e deve ter uma interface melhor.
    - O formulário de inserção da notícia arquivada deve ter manipuladores em javascript para restringir os campos quando o
      modo de inserção for alterado.

### Obsoleto

### REMOVIDO
- Não persista flags de modelo, utilize apenas o controller para definir, quando for salvar o modelo qual o
  processamento deve ser feito ou não.

### CORRIGIDO

### SEGURANÇA

## 0.1.0 - 2018-12-19

### ADICIONADO
- App dedicado para taxonomia
- Algumas anotações de tipo em variáveis
- App dedicado para documentos
  - Interface administrativa básica
- Uso da biblioteca `pylint-django`
- Classe `TraceableModel` com informações do usuário e timestamps para criação/modificação

- Meta: novos requisitos e changelog atualizado

## MODIFICADO
- Permita várias capturas de página por notícia arquivada
- Reorganização do changelog
- Toda mídia é um documento (classe `Document`)
  - Campo para captura em PDF agora é um relacionamento com o modelo `ArchivedNewsPDFCapture`
- Todos os modelos descendem de `TraceableModel`
- Reorganização dos arquivos para a interface de administração do app `archived_news`
- Classes das suítes dos testes deve herdar de `TransactionTestCase`
  - A suíte de testes `ArchivedNewsAdminFormTestCase` deve ser serial
- Alterações na interface do formulário de inclusão/edição de notícia arquivada
- Término do teste `test_fields_for_existing_item` para notícias arquivadas

## 0.0.0 - 2018-12-13

### Adicionado

#### Tipos de conteúdo

- Notícia arquivada

#### Auditoria

- Use a classe `LogEntry` do Django para manter um histórico de alterações
- Logue as seguintes ações realizadas para o STDOUT:
  - Jobs: `verify_if_in_archive_org`, `process_news` e `save_news_as_pdf`
  - Falhas de conexão com o Redis e trabalhos falhos

#### Captura

- Capture a notícia em formato PDF

#### Integração com o Archive.org

- Busque uma versão da notícia arquivada no Archive.org
