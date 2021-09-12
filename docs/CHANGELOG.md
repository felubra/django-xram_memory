Changelog
=========


1.5.0
------------

Adicionado
~~~~~~~~~~
- News listing endpoint (#160) [Felipe Lube de Bragança]

  * feat: install django rest framewor's token authentication

  * feat: new endpoint to get all the news info for static generation

  * feat: auth token endpoint

  * fix: update readme

Corrigido
~~~~~~~~~
- Rename file. [Felipe]

Outros
~~~~~~
- Chore(deps): bump pillow from 8.2.0 to 8.3.2 (#158) [dependabot[bot]]

  Bumps [pillow](https://github.com/python-pillow/Pillow) from 8.2.0 to 8.3.2.
  - [Release notes](https://github.com/python-pillow/Pillow/releases)
  - [Changelog](https://github.com/python-pillow/Pillow/blob/master/CHANGES.rst)
  - [Commits](https://github.com/python-pillow/Pillow/compare/8.2.0...8.3.2)

  ---
  updated-dependencies:
  - dependency-name: pillow
    dependency-type: direct:production
  ...
- Chore(deps): bump sqlparse from 0.4.1 to 0.4.2 (#159)
  [dependabot[bot]]

  Bumps [sqlparse](https://github.com/andialbrecht/sqlparse) from 0.4.1 to 0.4.2.
  - [Release notes](https://github.com/andialbrecht/sqlparse/releases)
  - [Changelog](https://github.com/andialbrecht/sqlparse/blob/master/CHANGELOG)
  - [Commits](https://github.com/andialbrecht/sqlparse/compare/0.4.1...0.4.2)

  ---
  updated-dependencies:
  - dependency-name: sqlparse
    dependency-type: indirect
  ...
- Chore(deps): bump pillow from 8.1.2 to 8.2.0 (#155) [dependabot[bot]]

  Bumps [pillow](https://github.com/python-pillow/Pillow) from 8.1.2 to 8.2.0.
  - [Release notes](https://github.com/python-pillow/Pillow/releases)
  - [Changelog](https://github.com/python-pillow/Pillow/blob/master/CHANGES.rst)
  - [Commits](https://github.com/python-pillow/Pillow/compare/8.1.2...8.2.0)

  ---
  updated-dependencies:
  - dependency-name: pillow
    dependency-type: direct:production
  ...
- Chore(deps): bump django from 2.2.20 to 2.2.24 (#157)
  [dependabot[bot]]

  Bumps [django](https://github.com/django/django) from 2.2.20 to 2.2.24.
  - [Release notes](https://github.com/django/django/releases)
  - [Commits](https://github.com/django/django/compare/2.2.20...2.2.24)

  ---
  updated-dependencies:
  - dependency-name: django
    dependency-type: direct:production
  ...
- Chore(deps): bump django from 2.2.19 to 2.2.20 (#151)
  [dependabot[bot]]

  Bumps [django](https://github.com/django/django) from 2.2.19 to 2.2.20.
  - [Release notes](https://github.com/django/django/releases)
  - [Commits](https://github.com/django/django/compare/2.2.19...2.2.20)
- Chore(deps): [security] bump django-debug-toolbar from 1.10.1 to
  1.11.1 (#152) [dependabot-preview[bot]]

  Bumps [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar) from 1.10.1 to 1.11.1. **This update includes a security fix.**
  - [Release notes](https://github.com/jazzband/django-debug-toolbar/releases)
  - [Changelog](https://github.com/jazzband/django-debug-toolbar/blob/1.11.1/docs/changes.rst)
  - [Commits](https://github.com/jazzband/django-debug-toolbar/compare/1.10.1...1.11.1)


1.4.1 (2021-03-28)
------------------

Adicionado
~~~~~~~~~~
- Abort app start if there is access error in lunr index folder. [Felipe
  Lube de Bragança]
- Allow download corpora to user folder. [Felipe Lube de Bragança]
- Otimizações no endpoint dos assuntos - Utilize um serializer mais
  simples e rápido para a maior dos casos - Obtenha objetos relacionados
  e guarde-os em cache - Somente pegue assuntos que tenham algum item
  relacionado - Remova campo não utilizado em SubjectSerializer. [Felipe
  Lube de Bragança]

Corrigido
~~~~~~~~~
- Revert django-elasticsearch-dsl update. [Felipe Lube de Bragança]
- Fix (Pipfile): use compatible release indicator. [Felipe Lube de
  Bragança]
- Fix(docs): add missing command to README.md. [Felipe Lube de Bragança]
- Get_file_icon: raise exception if no icon file is found. [Felipe Lube
  de Bragança]

Outros
~~~~~~
- Chore: update Pillow. [Felipe Lube de Bragança]
- Chore: update packages to avoid security issues. [Felipe Lube de
  Bragança]
- Chore: update cairosvg. [Felipe Lube de Bragança]
- Chore: update to DJango 2.2.19. [Felipe Lube de Bragança]
- Chore(docs): update readme with run instructions. [Felipe Lube de
  Bragança]
- Refactor: use try blocks in signal stopping decorators. [Felipe Lube
  de Bragança]
- Chore: readme: update install instructions. [Felipe Lube de Bragança]
- Chore(docs): update readme. [Felipe Lube de Bragança]
- Refactor: download_corpora: use boolean argument --user. [Felipe Lube
  de Bragança]
- Chore(deps): [security] bump djangorestframework from 3.11.1 to 3.11.2
  (#149) [dependabot-preview[bot]]

  Bumps [djangorestframework](https://github.com/encode/django-rest-framework) from 3.11.1 to 3.11.2. **This update includes a security fix.**
  - [Release notes](https://github.com/encode/django-rest-framework/releases)
  - [Commits](https://github.com/encode/django-rest-framework/compare/3.11.1...3.11.2)
- Chore(deps): [security] bump lxml from 4.5.2 to 4.6.2 (#146)
  [dependabot-preview[bot]]

  Bumps [lxml](https://github.com/lxml/lxml) from 4.5.2 to 4.6.2. **This update includes a security fix.**
  - [Release notes](https://github.com/lxml/lxml/releases)
  - [Changelog](https://github.com/lxml/lxml/blob/master/CHANGES.txt)
  - [Commits](https://github.com/lxml/lxml/compare/lxml-4.5.2...lxml-4.6.2)
- Refactor: um gerenciador de contexto não precisa ser uma fixture.
  [Felipe Lube de Bragança]
- Chore: limpeza nas importações e remoção de arquivos inúteis. [Felipe
  Lube de Bragança]
- Refactor: Não filtre a saída do endpoint das palavras-chave. [Felipe
  Lube de Bragança]

  BREAKING CHANGE

  A responsabilidade pela filtragem das palavras-chave irrelevantes é de quem as insere no banco de dados
- Merge branch 'dev' of github.com:felubra/django-xram_memory into dev.
  [Felipe Lube de Bragança]
- Reestilização do formulário p/ adicionar várias notícias (#142)
  [Felipe Lube de Bragança]

  * chore: atualização no arquivo .env de exemplo

  * feat: breadcrumbs

  * refat: move o formulário para o módulo dos formulários

  * feat: estilização do formulário p/ adicionar várias notícias
  -  Breadcrumbs
  - Textarea deve ficar alinhada abaixo do label
  - Campo endereços deve ser (estilizado como) obrigatório
  - Botão submit deve ser renomeado para 'Inserir notícias'
  - Label de ajuda, logo abaixo do textarea deve ficar alinhado com
  o textarea
  - Barra de botões no final

  * feat: aumente o tamanho da textarea
- Chore: atualização no arquivo .env de exemplo. [Felipe Lube de
  Bragança]
- Chore: atualização de README.md. [Felipe Lube de Bragança]
- Chore: atualização de changelog. [Felipe Lube de Bragança]


1.4.0 (2020-10-12)
------------------

Adicionado
~~~~~~~~~~
- [lunr] comando básico para a reconstrução do índice. [Felipe Lube de
  Bragança]
- [lunr] failback para a data de modificação sem data de publicação.
  [Felipe Lube de Bragança]
- Endpoint para obter artefatos associados a um assunto - atualização no
  endpoint similar para palavras-chave. [Felipe Lube de Bragança]
- Endpoint para artefatos associados a um termo de taxonomia. [Felipe
  Lube de Bragança]

  close #135
- Endpoint para artefatos associados a um termo de taxonomia - close
  #135. [Felipe Lube de Bragança]
- #132 Endpoint para as palavras-chave e a contagem de notícias
  associada. [Felipe Lube de Bragança]

  feat: #132 Endpoint para as palavras-chave e a contagem de notícias associada
- Endpoint para as palavras chave mais associadas - permita definir um
  limite através do parâmetro `max` [Felipe Lube de Bragança]
- Utilize o Memcached como backend do cache com failback. [Felipe Lube
  de Bragança]
- Entrypoint para retornar palavras-chave mais usadas e contagem.
  [Felipe Lube de Bragança]
- Multi stage build (#131) [Felipe Lube de Bragança]

  * chore: configurações separadas para apps de indexação distintos
  - IndexingWithLunrSearch: indexação somente com o (Elastic)Lunr
  - IndexingWithElasticSearch: indexação com o ElasticSearch
  - IndexingWithAllApps: indexação com os dois apps
  - Development: configuração para desenvolvimento com os 2 apps ligados
  - Staging continua usando apenas o app do ElasticSearch

  * feat: atualizações na imagem docker
  - Build multi-stage com suporte para ambiente de desenvolvimento
  - Use node:lts-alpine ao invés de node:8
  - Atualize o SO do python para debian buster
  - Correção no link de download do wkhtmltox
  - Redução de ~550MB no tamanho da imagem

  * chore: renomeie os estágios do build do container

  * chore: ignore os arquivos do docker na imagem

  * chore (docker): correção no estágio de desenvolvimento

  * chore: use o endereço de desenvolvimento em homologação por padrão
  - definição da configuração ALLOWED_HOSTS via env var

  * feat: configuração para rodar em desenvolvimento via docker

  * fix: desabilte o http retry em lunr_index_rebuild por enquanto

  * fix: retorne o cliente em _get_client
- Feat(dev): atualização do script entrypoint - permita a execução do
  servidor de desenvolvimento do Django. [Felipe Lube de Bragança]
- Feat(dev): permita debugar app e testes remotamente. [Felipe Lube de
  Bragança]

Corrigido
~~~~~~~~~
- Corrige a semântica dos endpoints (#140) [Felipe Lube de Bragança]

  * refat: utilize uma constanta para a base da API

  * fix: REST: a filtragem das páginas deve ser vai url params

  * fix: correção nos endpoints de taxonomia
  - filtragem de tipos e ordenação deve ser feita por query params
- Use o failback cache em todas as configurações, exceto em staging.
  [Felipe Lube de Bragança]
- Afrouxe os requisitos para algumas variáveis para setar o app do lunr.
  [Felipe Lube de Bragança]
- Remova pass inútil. [Felipe Lube de Bragança]
- Não carregue o debugger remoto se somente DEBUG=True. [Felipe Lube de
  Bragança]
- Adicione os arquivos em fata do jquery/ui. [Felipe Lube de Bragança]
- Limite o título ao tamanho máximo do campo. [Felipe Lube de Bragança]

Outros
~~~~~~
- Merge pull request #139 from felubra/elastic-lunr-staging. [Felipe
  Lube de Bragança]

  chore: use a indexação ElasticLunr ao invés do ElasticSearch em homologação
- Chore: use a indexação lunr ao invés do elasticsearch em homologação.
  [Felipe Lube de Bragança]
- Merge pull request #138 from felubra/fix-cache. [Felipe Lube de
  Bragança]

  fix: use o failback cache em todas as configurações, exceto em staging
- Chore: logue caso não consiga obter o lock. [Felipe Lube de Bragança]
- Merge branch 'dev' into issue-132. [Felipe Lube de Bragança]
- Revert "chore: atualização da imagem do docker" [Felipe Lube de
  Bragança]

  This reverts commit a5f7a5b65ad9cbe59b15c3de6e847f02c6b28566.
- Merge branch 'issue-127' into dev. [Felipe Lube de Bragança]
- Chore: atualização do endereço local. [Felipe Lube de Bragança]
- Chore: atualização da imagem do docker. [Felipe Lube de Bragança]


1.3.0 (2020-07-13)
------------------

Adicionado
~~~~~~~~~~
- Gerenciador de contexto para desabilitar sinais de artifact. [Felipe
  Lube de Bragança]
- Refatore os builders como classes. [Felipe Lube de Bragança]
- Funcionalidade de um processador de sinais plugável. [Felipe Lube de
  Bragança]
- Suporte a alteração temporária dos plugins de um registro -
  refatoração da fixture news_fetcher_plugin_factory, agora um
  gerenciador de contexto - adaptação dos testes ao uso da nova forma
  fixture. [Felipe Lube de Bragança]
- Teste para verificar utilização de plugins de captura - testes não
  podem ser executados no momento, pois outros testes poluíram o
  registro de plugins. [Felipe Lube de Bragança]
- Processador de sinais para o ES que evita a execução em importação de
  fixtures - decorador disable_for_loaddata - reestruturaçao do modulo
  xram_memory.utils - utilizaçao do decorador novo em todos os receivers
  da aplicaçao. [Felipe Lube de Bragança]
- Desative aplicativos de indexação nos testes em que eles não são
  necessários. [Felipe Lube de Bragança]
- Funções, mixins e decoradores para desabilitar sinais dos aplicativos
  de indexação. [Felipe Lube de Bragança]
- Processador de sinais desligável em lunr_search - encapsule o
  funcionamento dos sinais num objeto, de forma a permitir a
  conexão/desconexão dos sinais em runtime, o que será usado nos testes.
  [Felipe Lube de Bragança]
- Retrinja os sinais aos modelos. [Felipe Lube de Bragança]
- Permita desabilitar os sinais para indexação do lunr. [Felipe Lube de
  Bragança]
- Envio de requisições robusto com tentativas. [Felipe Lube de Bragança]
- Testes. [Felipe Lube de Bragança]
- Função para transformar uma datetime em string. [Felipe]
- Suporte à configuração via variáveis-ambiente. [Felipe]
- Adequação ao novo esquema de requisição; alteração em configuração -
  simplifique o nome das configurações - configuração para definir quais
  campos indexar - alteração na requisição enviada ao serviço externo,
  sendo objeto com   - os itens a indexar   - os campos que serão
  indexados   - se o documentos devem ser salvos no índice. [Felipe]
- Feat(wip): suporte ao envio documentos via http. [Felipe]
- Adicione um campo para o cliente gerar a url do item. [Felipe]
- #112 adicione suporte a geraçao de um indice lunr. [Felipe Lübe de
  Bragança]

  * chore: adicione lunr e lunr[languages]

  * feat: #112 construção de app com escutador de sinal
  - Escutador de sinal para agendar a execução de uma task assíncrona
  toda vez que os conteúdos do site atualizarem

  * chore: #112 renomeie app

  * feat: #112 defina as configurações, parâmetros para a geração do índice

  * feat: #112 parametrize a task com a configuração do app

  * chore: #112 instale suporte ao memcached

  * chore: #112 defina explicitamente a configuração dos caches

  * feat: sistema de armazenamento que sobrescreve arquivo

  * feat: #112 corpo da função da task para gerar um índice

  * chore: #112 defina a url de conexão ao memcached via variável-ambiente

  * feat: #112 garanta a execução de apenas um task para geração do índice
  - NOTA: atomicidade só é garantida com o backend memcached

  * fix: ajustes no decorador de logging
  - obtenção safa de obj
  - não 'Artefato' como failback para valor do tipo do item alterado

  * feat: #112 logging básico no sinal

Corrigido
~~~~~~~~~
- Correção da assinatura de lunr_index_rebuild. [Felipe Lube de
  Bragança]
- Limpa o cache de funções que utilizam lru_cache antes dos testes.
  [Felipe Lube de Bragança]
- Correção em assinatura de task. [Felipe]
- Não tente gerar o índice elastic_lunr novamente quando executado
  sincronamente. [Felipe Lube de Bragança]
- Correção em schedule_lunr_index_rebuild; documentação. [Felipe Lube de
  Bragança]
- NewsFactory desabilite campos que precisam de factory específico.
  [Felipe Lube de Bragança]
- Lunr_index_rebuild: sempre verifique o valor das configurações em
  runtime. [Felipe Lube de Bragança]
- Verifique se a notícia tem jornal antes de tentar adicioná-lo. [Felipe
  Lube de Bragança]
- Queryset correto para documentos. [Felipe]
- Chame corretamente a task no modo síncrono. [Felipe]

Outros
~~~~~~
- Merge pull request #129 from felubra/issue-127. [Felipe Lube de
  Bragança]

  Issue 127 - Suporte a geração de índices elastic-lunr
- Chore: acelere os testes em test_localsearch. [Felipe Lube de
  Bragança]
- Refat: empacote os sinais de artifact numa classe processadora.
  [Felipe Lube de Bragança]
- Refat: utilize xram_memory.utils.classes.SignalProcessor. [Felipe Lube
  de Bragança]
- Chore: habilite 2 testes. [Felipe Lube de Bragança]
- Chore: documentações nos testes e pequenas correções. [Felipe Lube de
  Bragança]
- Merge branch 'dev' into issue-127. [Felipe Lube de Bragança]
- Chore: atualização do Django e outros pacotes. [Felipe]
- Chore: configuração do pytest. [Felipe Lube de Bragança]
- Chore: scripts para rodar testes. [Felipe Lube de Bragança]
- Chore: exclusão de arquivo de cobertura. [Felipe Lube de Bragança]
- Chore: lembrete de fixme. [Felipe Lube de Bragança]
- Chore: atualização de pacotes. [Felipe Lube de Bragança]
- Chore: extraia função utilitária de teste. [Felipe Lube de Bragança]
- Revert "config: deabilite o app django_elasticsearch_dsl" [Felipe Lube
  de Bragança]

  This reverts commit 89cc3be99bb7fa40876b8f26654e2f9d696f6e81.
- Refat: separe o código que cria o índice do código da task de criação.
  [Felipe]
- Refat: refatore lunr_index_rebuild - índice único para documentos e
  notícias - permita a geração de um índice vazio - adicione os campos
  newspaper, thumbnail, published_date. [Felipe]
- Config: deabilite o app django_elasticsearch_dsl. [Felipe]
- Chore: identificação de bug. [Felipe]
- Refat: exigência condicional de variáveis-ambiente; uso de constantes
  - use constantes para lidar com o backend gerador do índice - não
  exija LUNR_INDEX_REMOTE_SECRET e LUNR_INDEX_REMOTE_HOST se o backend
  for local - redefina o backend padrão para BACKEND_LOCAL. [Felipe]


1.2.3 (2020-04-19)
------------------

Corrigido
~~~~~~~~~
- #119 remova cache dos endpoints dos Assuntos; doc. problemas de cache
  (#123) [Felipe Lübe de Bragança]


1.2.2 (2020-04-19)
------------------

Corrigido
~~~~~~~~~
- #111 ordenação correta ao buscar capa do álbum (#122) [Felipe Lübe de
  Bragança]
- #120 correção em endpoint dos assuntos (#121) [Felipe Lübe de
  Bragança]

  - ordenação natural dos assuntos pela slug feita em python
  - remoção de itens acentuados da inicial '!"

Outros
~~~~~~
- Chore(deps): bump django from 2.2.9 to 2.2.10 (#94) [dependabot[bot]]

  Bumps [django](https://github.com/django/django) from 2.2.9 to 2.2.10.
  - [Release notes](https://github.com/django/django/releases)
  - [Commits](https://github.com/django/django/compare/2.2.9...2.2.10)


1.2.1 (2020-01-17)
------------------

Adicionado
~~~~~~~~~~
- Atualização para o Django 2.2 (#91) [Felipe Lübe de Bragança]

  * feat: atualize o django para 2.2.9 e os outros pacotes

  * chore: use a versão binária de psycopg2

  * chore: ajuste em pacote que não pode ser atualizado


1.2.0 (2020-01-13)
------------------

Corrigido
~~~~~~~~~
- Fix (close #87): desabilite o autocrop para visualizações. [Felipe]

Outros
~~~~~~
- Chore: atualização de segurança do django 2.1.5 e outros pacotes.
  [Felipe]
- Chore (js): atualização de segurança para quill 1.37. [Felipe]


1.1.7 (2020-01-03)
------------------

Adicionado
~~~~~~~~~~
- Retorne informações sobre o documento da imagem da notícia. [Felipe
  Lube de Bragança]
- Adicione campos necessários à ordenação no frontend - adicione um
  alias 'published_date' para o campo 'modiefied_at' em Document -
  adicione um campo 'raw' para o campo title. [Felipe Lube de Bragança]

Corrigido
~~~~~~~~~
- Close #82 instalação de pytest-ordering, que estava ausente. [Felipe
  Lube de Bragança]

Outros
~~~~~~
- Chore: git - ignore todos os arquivos de banco de dados. [Felipe Lube
  de Bragança]


1.1.6 (2019-11-19)
------------------

Corrigido
~~~~~~~~~
- Fixe python em 3.7 para compatibilidade com o psycopg2. [Felipe Lube
  de Bragança]

Outros
~~~~~~
- Chore: trave psycopg2 em < 2.8. [Felipe Lube de Bragança]


1.1.5 (2019-10-29)
------------------

Corrigido
~~~~~~~~~
- Verifique corretamente se é uma instância de Documento. [Felipe Lube
  de Bragança]
- Verifique corretamente se é uma instância de Documento. [Felipe Lube
  de Bragança]
- Fixes #71 documentos que não são do usuário não devem ser indexados.
  [Felipe Lube de Bragança]

Outros
~~~~~~
- Chore: atualização de segurança do Pillow. [Felipe Lube de Bragança]
- Merge branch 'dev' of https://github.com/felubra/django-xram_memory
  into dev. [Felipe Lube de Bragança]
- Chore: remoção de arquivos vazios na pasta de testes. [Felipe Lube de
  Bragança]
- Chore: atualização para django 2.1.13 e outros pacotes de produção.
  [Felipe Lube de Bragança]
- Chore: atualização de dependências dev e travamento de dep. de
  produção. [Felipe Lube de Bragança]
- Chore: atualização de segurança para Werkzeug. [Felipe Lube de
  Bragança]
- Chore: atualizações de pacotes. [Felipe Lube de Bragança]


1.1.4 (2019-08-18)
------------------

Adicionado
~~~~~~~~~~
- Link para a notícia publicada no site. [Felipe Lube de Bragança]

Corrigido
~~~~~~~~~
- Correção em get_absolute_url para incluir a barra inicial. [Felipe
  Lube de Bragança]


1.1.3 (2019-08-18)
------------------

Outros
~~~~~~
- Merge branch 'dev' [Felipe Lube de Bragança]
- Chore: atualização de segurança do Django para 2.1.11. [Felipe Lube de
  Bragança]


1.1.2 (2019-07-30)
------------------

Corrigido
~~~~~~~~~
- Retorne listas vazias ao invés de um erro 404. [Felipe Lube de
  Bragança]

Outros
~~~~~~
- Merge branch 'dev' [Felipe Lube de Bragança]
- Merge branch 'dev' [Felipe Lube de Bragança]


1.1.1 (2019-07-27)
------------------

Corrigido
~~~~~~~~~
- Correção nas views da iniciais: use ! ao invés de # [Felipe Lube de
  Bragança]


1.1.0 (2019-07-27)
------------------

Adicionado
~~~~~~~~~~
- Adicione django-rest-multiple-models. [Felipe Lube de Bragança]
- Acesso aos assuntos pela(s) inicial(is) [Felipe Lube de Bragança]
- Use todos os tamanhos de imagem para todos os modelos em thumbnails.
  [Felipe Lube de Bragança]
- Inclua tods os thumbnails no serializer da notícia. [Felipe Lube de
  Bragança]
- Endpoint para o assunto pela slug. [Felipe Lube de Bragança]
- Não habilite o cache da view se em debug. [Felipe Lube de Bragança]
- Sianis para criar e salvar um objeto Álbum quando salvar a pasta de
  álbum. [Felipe Lube de Bragança]
- Is_album_folder para determinar se uma pasta é uma pasta de álbum de
  fotos. [Felipe Lube de Bragança]
- A chave primária do álbum é o id da pasta. [Felipe Lube de Bragança]
- Modelo com campos específicos para um Álbum. [Felipe Lube de Bragança]
- Mais visualizações. [Felipe Lube de Bragança]
- API: forneça uma imagem de capa grande para um assunto. [Felipe Lube
  de Bragança]
- API: forneça uma capa para um álbum. [Felipe Lube de Bragança]
- Retorne apenas assuntos que têm itens associados. [Felipe Lube de
  Bragança]
- Quantidad e de itens associada ao assunto. [Felipe Lube de Bragança]
- Endpoint para a página de assuntos. [Felipe Lube de Bragança]
- Adicione uma nova imagem de pré-visualização para documentos. [Felipe
  Lube de Bragança]
- Suporte para descrição de um assunto. [Felipe Lube de Bragança]
- Retorno e melhor suporte aos assuntos - assuntos são extraidos das
  palavras-chave dos parsers - assuntos são diferenciados das palavras-
  chave por terem palavras compostas - cobertura de teste para assuntos
  - reativação dos assuntos na interface administrativa - melhor uso do
  Goose3NewspaperArticleParser para extrair assuntos. [Felipe Lube de
  Bragança]
- Página: permita indicar se link na página inicial. [Felipe Lube de
  Bragança]

Corrigido
~~~~~~~~~
- Verifique se há escolhas antes de tentar escolher. [Felipe Lube de
  Bragança]
- Ajustes nos tamanhos das imagens geradas e mais um estilo. [Felipe
  Lube de Bragança]
- Correção em is_album_folder. [Felipe Lube de Bragança]
- Não exija que o usuário cliquem adicionar Album no formulário
  adminsitrativo. [Felipe Lube de Bragança]
- Correção na chamada da propriedade has_description. [Felipe Lube de
  Bragança]
- Adicione dependência usada por no_empty_html. [Felipe Lube de
  Bragança]
- Correção em arquivo utilizado em teste. [Felipe Lube de Bragança]
- Remova de vez os assuntos da interface administrativa. [Felipe Lube de
  Bragança]

Outros
~~~~~~
- Chore: adicione pip-licenses para gerar info sobre as licenças usadas.
  [Felipe Lube de Bragança]
- Refat: simplifique a definição de um assunto em destaque com um campo
  para tanto. [Felipe Lube de Bragança]
- Chore: use dockerfile maiusculo. [Felipe Lube de Bragança]
- Chore: use multi-estágios docker para construir a imagem. [Felipe Lube
  de Bragança]
- Refat: unifique as visualizações geradas para notícias e documentos.
  [Felipe Lube de Bragança]
- Chore: atualização de segurança para o Django 2.1.10. [Felipe Lube de
  Bragança]
- Refat: use uma única propriedade cacheada, fonte dos thumbnails.
  [Felipe Lube de Bragança]
- Refat: mova no_empty_html para o módulo xram_memory.utils. [Felipe
  Lube de Bragança]
- Refat: organize o código que gera um editor de texto rico. [Felipe
  Lube de Bragança]


1.0.0 (2019-06-17)
------------------

Adicionado
~~~~~~~~~~
- (closes #74) desabilita os assuntos na interface administrativa.
  [Felipe Lube de Bragança]
- Adicione a biblioteca libmagic como dependência no Windows. [Felipe
  Lube de Bragança]
- Permita imagens e links no texto da chamada da página. [Felipe Lube de
  Bragança]
- Suporte para textos de chamada de página customizados. [Felipe Lube de
  Bragança]
- Suporte a notícias associadas a um documento. [Felipe Lube de
  Bragança]
- Tests: adicione factories para News e Newspaper. [Felipe Lube de
  Bragança]
- Adicione o ipython para um experiência com terminal melhor. [Felipe
  Lube de Bragança]
- Concentração de diretórios num só; estilo pytest. [Felipe Lübe de
  Bragança]
- Newsfetcher: sistema de plugins para capturas, arquivos e informações
  básicas; correções diversas. [Felipe Lübe de Bragança]

  * Reestruturação dos diretórios: lugar próprio para a biblioteca news_fetcher
  * Inclusão de vários testes para NewsFetcher e alteração/expansão dos testes existentes
  * Sistema de plugins em NewsFetcher:
  - utilize plugins para buscar uma versão arquivada da notícia
  - utilize plugins para capturar a página da notícia
    - capturador padrão e um especialista (G1) para páginas em PDF (closes #69 e closes #68)
  - captura de informações básicas implementada via plugins
  * Utilize um hashid como nome de arquivo para um logotipo de jornal
  * NPM_FILE_PATTERNS: padrões de caminhos de acordo com a plataforma
  * Migração do sistema de testes para o pytest [WIP]
- Testes para newspaper (100%) [Felipe Lube de Bragança]
- Expansão da cobertura dos testes de News (100%) [Felipe Lube de
  Bragança]
- Refatoração dos testes para o modelo News - 65% de cobertura - remoção
  dos testes de NewsAdmin por enquanto. [Felipe Lube de Bragança]
- (docs) documentação dos testes de documento; melhoria de um. [Felipe
  Lube de Bragança]
- Testes para documento (100% de cobertura) [Felipe Lube de Bragança]
- Adicione bibliotecas para auxílio na feitura e cobertura de testes.
  [Felipe Lube de Bragança]
- (adm) Ações em massa para Notícias, closes #47. [Felipe Lube de
  Bragança]
- Menor uso de memória do worker do celery. [Felipe Lube de Bragança]
- Closes #62 informaçoes sobre captura em pdf; nao logue wkhtmltopdf no
  console. [Felipe Lube de Bragança]
- Adicione uma data de publicação original em Documento. [Felipe Lube de
  Bragança]
- Set_document_info: Somente salve o modelo se de fato ao menos uma
  operação foi executada com sucesso. [Felipe Lube de Bragança]
- Comando administrativo para determinar mime_type de documentos.
  [Felipe Lube de Bragança]
- Utilizes campos com nomes comuns entre os dois índices para facilitar
  filtragem no cliente. [Felipe Lube de Bragança]
- Defina o tipo do documento do índice para permitir filtragens no
  cliente. [Felipe Lube de Bragança]
- Faça um índice para os documentos no elastic_search. [Felipe Lube de
  Bragança]
- Adicione palavras-chave e assuntos aos documentos. [Felipe Lube de
  Bragança]
- Comando administrativo para geração de document_id para todos
  documentos. [Felipe Lube de Bragança]
- Indexe o favicon do jornal. [Felipe Lube de Bragança]
- (closes #55): usar hashs ao invés de ids nas urls da API. [Felipe Lube
  de Bragança]
- Logue erros por padrao no console. [Felipe Lube de Bragança]
- Aumente o tamanho dos uploads para 10.5MB. [Felipe Lube de Bragança]
- Não execute o container como root. [Felipe Lube de Bragança]
- Instale o corpora do NLTK num local de sistema mas acessível para
  outros usuários. [Felipe Lube de Bragança]
- Conexão autenticada ao servidor do ElasticSearch. [Felipe Lube de
  Bragança]
- Colete os arquivos estáticos primeiro para dar chance, quem sabe, do
  db ter iniciado. [Felipe Lube de Bragança]
- Mova a instalação do node para o topo, de forma a usar melhor o cache.
  [Felipe Lube de Bragança]
- Defina a url do servidor do ES via env var. [Felipe Lube de Bragança]
- Feat (dockerfile): separe os downloads pesados em estágio próprio.
  [Felipe Lube de Bragança]
- Nova imagem docker. [Felipe Lube de Bragança]
- Adicione suporte ao Mysql/MariaDB. [Felipe Lube de Bragança]
- Libere um endereço local em ALLOWED_HOSTS. [Felipe Lube de Bragança]
- Atualização da imagem do docker -  instalação de módulos npm - script
  entrypoint com execução de migrações. [Felipe Lube de Bragança]

Corrigido
~~~~~~~~~
- Downgrade em django-current-user para evitar problemas com o django
  2.1.9. [Felipe Lube de Bragança]
- Marque testes que irão usar o banco de dados. [Felipe Lube de
  Bragança]
- Adicione o timestamp dos recursos nos endpoints da api. [Felipe Lube
  de Bragança]
- Apague o arquivo do documento ao se apagar uma captura. [Felipe Lube
  de Bragança]
- (closes #67) use um sal para gerar um nome de arquivo. [Felipe Lube de
  Bragança]
- Newspaper: string padrão. [Felipe Lube de Bragança]
- Newspaper: refatoração de funções para a filosofia EAFP. [Felipe Lube
  de Bragança]
- Refatoração de has_pdf_capture e has_image. [Felipe Lube de Bragança]
- Um título provisório qdo não houver título. [Felipe Lube de Bragança]
- Limpe o cache de thumbnails se um documento for salvo. [Felipe Lube de
  Bragança]
- Remoção de constantes de config. não usadas mais. [Felipe Lube de
  Bragança]
- Documents: refatoramento pela filosofia EAFP após testes. [Felipe Lube
  de Bragança]
- Corrija o modo de leitura de determine_mime_type() [Felipe Lube de
  Bragança]
- Remova um construtor customizado do qual não precisamos. [Felipe Lube
  de Bragança]
- Chame corretamente a função now. [Felipe Lube de Bragança]
- Set_document_info() verifique pelo atributo antes de deletá-lo.
  [Felipe Lube de Bragança]
- Feche corretamente o arquivo em determine_mime_type() - retorne um
  resultado para determinar se a operação encontrou um novo mime_type.
  [Felipe Lube de Bragança]
- Somente indexe documentos públicos e inseridos manualmente pelo
  usuário. [Felipe Lube de Bragança]
- Defina is_user_object (documento) em processos automáticos. [Felipe
  Lube de Bragança]
- Ordene itens de taxonomia pelo nome por padrão. [Felipe Lube de
  Bragança]
- (closes #46) largura mínima para área de ícones de captura. [Felipe
  Lube de Bragança]
- Correção na geração do favicon do logo do jornal; mudança no nome do
  campo. [Felipe Lube de Bragança]
- Workaround para o problema do jquery-ui que falta. [Felipe Lube de
  Bragança]
- Aumente o timeout do gunicorn para operaçoes longas. [Felipe Lube de
  Bragança]
- Logue apenas erros para o console em dev. [Felipe Lube de Bragança]
- Limite a inserção de conteúdo que ultrapassaria o limite do campo no
  BD. [Felipe Lube de Bragança]
- Closes #50 retorne a própria url se não for possível obter um título.
  [Felipe Lube de Bragança]
- Fix (docker): adicione o pacote poppler-utils, necessário para pré-
  visualizações de arquivos pdf. [Felipe Lube de Bragança]
- Remoção do campo slug em NewspaperSerializer. [Felipe Lube de
  Bragança]
- Permita a definição de CELERY_BROKER_URL por variável-ambiente.
  [Felipe Lube de Bragança]

Outros
~~~~~~
- Merge branch 'dev' [Felipe Lube de Bragança]
- Chore: atualização de pacotes. [Felipe Lube de Bragança]
- Chore: atualização de pacotes js. [Felipe Lube de Bragança]
- Chore: ajustes no pipfile - remoção da bilioteca do mysql - use
  django-currentuser do repositório do pipy não do github - torne a
  definição do django compatível com django-currentuser. [Felipe Lube de
  Bragança]
- Chore: limpeza e reorganização dos testes. [Felipe Lube de Bragança]
- Merge pull request #61 from felubra/documents_in_index. [Felipe Lübe
  de Bragança]

  Adicione os documentos enviados pelo usuário ao índice
- Merge branch 'dev' into documents_in_index. [Felipe Lube de Bragança]
- Merge branch 'dev' of https://github.com/felubra/django-xram_memory
  into dev. [Felipe Lube de Bragança]
- Nunca permita o cache da view para inserção múltipla. [Felipe Lube de
  Bragança]
- Merge branch 'dev' of https://github.com/felubra/django-xram_memory
  into dev. [Felipe Lube de Bragança]
- Chore: atualize o changelog para versão 0.8.0. [Felipe Lube de
  Bragança]
- Chore: atualização no .gitignore. [Felipe Lube de Bragança]


0.8.0 (2019-04-21)
------------------

Adicionado
~~~~~~~~~~
- Testes básicos para newspaper. [Felipe Lube de Bragança]
- Formulários e ações adm para adm de Jornais - Formulário
  administrativo para o Jornal com possibilidade de adicionar info e
  logo (closes #48) - Ações em massa para lidar com logotipos de
  formulário (closes #48) - Tarefa para adicionar logotipo a Jornal -
  Logue ações de Jornal - set_logo_from_favicon mais robusta - flag para
  verificar se o jornal tem um logo. [Felipe Lube de Bragança]
- Generalização de determine_additional_tasks_to_run. [Felipe Lube de
  Bragança]
- Otimização de consultas à modelos relacionados. [Felipe Lube de
  Bragança]
- Newspaper: grave um logotipo de um favicon capturado - closes #48.
  [Felipe Lube de Bragança]
- Remoção de python-magic-bin - pacote estava travando o lock. [Felipe
  Lube de Bragança]
- Cacheie o objeto da pasta de álbuns. [Felipe Lube de Bragança]
- Retorne os thumbnails disponíveis para cada foto do álbum. [Felipe
  Lube de Bragança]
- Geração de pré-visualizações adicionais para documentos de imagem.
  [Felipe Lube de Bragança]
- Endpoint para os álbuns, que nada são do que pastas. [Felipe Lube de
  Bragança]
- Defina as pastas como dicionários / estrutura hierárquica. [Felipe
  Lube de Bragança]
- Migração de dados para criar pastas-padrão. [Felipe Lube de Bragança]
- Utilize constantes para os nomes das pastas. [Felipe Lube de Bragança]
- Remova campos não usados pelo jornal. [Felipe Lube de Bragança]
- Interface administrativa básica para jornais / sites. [Felipe Lube de
  Bragança]
- Comando administrativo para apagar miniaturas do app artifact. [Felipe
  Lube de Bragança]
- Miniatura específica para documentos. [Felipe Lube de Bragança]
- Closes #34: verificações adicionais antes de iniciar a aplicação -
  Testes devem acontecer apenas com o 'check --deploy' - Verifique
  conexão com o Elasticsearch - Verifique libmagic, wkhtmltopdf, ntlk e
  seu corpus. [Felipe Lube de Bragança]
- Pool de execução do celery no windows mudado para gevent. [Felipe Lube
  de Bragança]
- Suporte definição de CELERY_BROKER_URL via variável ambiente. [Felipe
  Lube de Bragança]
- Closes #40 : não permita inserção múltipla sem servidor de filas.
  [Felipe Lube de Bragança]
- Centralize o logo na tela de login. [Felipe Lube de Bragança]
- Mostre o logo na interface administrativa. [Felipe Lube de Bragança]
- Ícones de status das capturas usando a fonte material-icons. [Felipe
  Lube de Bragança]
- Feat: decore a função io intensiva  get_file_icon() com @lru_cache.
  [Felipe Lube de Bragança]
- Indicação das capturas de um item na Lista de notícias. [Felipe Lube
  de Bragança]
- Botão para inserir múltiplas notícias  lado-a-lado com outro botão.
  [Felipe Lube de Bragança]

  - Movida a view para inserção múltima para NewsAdmin
- Flutue a linha de açẽos do formulário de edição/adição. [Felipe Lube
  de Bragança]
- Utilize os campos do filer nos modelos de captura. [Felipe Lube de
  Bragança]
- Exclua o campo original_url em NewsImageCaptureStackedInlineForm.
  [Felipe Lube de Bragança]
- Unificação dos campos de captura em TabularInline. [Felipe Lube de
  Bragança]
- Integração inicial com o django-tags-input. [Felipe Lube de Bragança]

Corrigido
~~~~~~~~~
- Correção em has_basic_info, deve haver ao menos um título. [Felipe
  Lube de Bragança]
- Invoque o BeautifulSoup com um parser definido. [Felipe Lube de
  Bragança]
- Correção em nome de função. [Felipe Lube de Bragança]
- Correção na herança de Newspaper. [Felipe Lube de Bragança]
- Utilize o serializer do documento inteiro em
  PhotoAlbumFolderSerializer. [Felipe Lube de Bragança]
- Forneça a url do arquivo original também. [Felipe Lube de Bragança]
- Fix(closes #45): Uma pasta vazia não pode ser considerada como álbum.
  [Felipe Lube de Bragança]
- Force a geração e a indexação correta do thumbnail da notícia. [Felipe
  Lube de Bragança]
- Simplificação nos nomes dos tamanhos. [Felipe Lube de Bragança]
- Correção na url do álbum individual. [Felipe Lube de Bragança]
- Se o documento não tiver nome, use o nome do arquivo. [Felipe Lube de
  Bragança]
- Correção no nome da constante. [Felipe Lube de Bragança]
- Correção na criação das pastas quando das criação das capturas.
  [Felipe Lube de Bragança]
- Reconfiguração do thumbnail gerado para notícias. [Felipe Lube de
  Bragança]
- Adicione greenlet, necessário à execução do celery no windows. [Felipe
  Lube de Bragança]
- Acerte a geração de thumbnails. [Felipe Lube de Bragança]
- Corrija o tamanho do texto de ajuda. [Felipe Lube de Bragança]
- Mova get_file_icon para utils.py. [Felipe Lube de Bragança]
- Correção de problemas na geração de arquivos estáticos - Utilize uma
  versão modificada de ManifestStaticFilesStorage para suportar
  corretamente o parsing de arquivo css com comentários - Utilize
  caminhos em formato POSIX em NPM_FILE_PATTERNS. [Felipe Lube de
  Bragança]
- Tagsinput: sem altura 40px e placeholder pt. [Felipe Lube de Bragança]
- Correção no nome do campo url. [Felipe Lube de Bragança]
- Não verifique por uma slug no modo de edição. [Felipe Lube de
  Bragança]

Outros
~~~~~~
- Chore: atualização de pacotes. [Felipe Lube de Bragança]
- Merge branch 'photo_album' into newspaper_admin. [Felipe Lube de
  Bragança]
- Chore: refeitura do pipfile, dessa vez mais conservador. [Felipe Lube
  de Bragança]
- Merge pull request #42 from felubra/app_checks. [Felipe Lübe de
  Bragança]

  feat: closes #34: verificações adicionais antes de iniciar a aplicação
- Chore: atualização do changelog. [Felipe Lube de Bragança]
- Merge pull request #41 from felubra/admin_fixes. [Felipe Lübe de
  Bragança]

  Closes #32


0.7.0 (2019-03-22)
------------------

Adicionado
~~~~~~~~~~
- Remova o widget customizado em DocumentAdmin. [Felipe Lube de
  Bragança]
- Icon_preview: retorne ícone de arquivo em branco como failback.
  [Felipe Lube de Bragança]
- Document: modelo do app Filer com nossas customizações. [Felipe Lube
  de Bragança]
- Traduza o nome padrão do app filer no admin. [Felipe Lube de Bragança]
- Adote um ratelimit global para os endpoints da API. [Felipe Lube de
  Bragança]
- Renomeie, para o usuário, o campo slug para endereço. [Felipe Lube de
  Bragança]
- NewsAdminForm: valide a presença duma slug no modo manual. [Felipe
  Lube de Bragança]
- NewsAdminForm: descrições diferentes de acordo com estado modelo.
  [Felipe Lube de Bragança]
- Feat: @log_process: infira o nome humano do modelo automaticamente.
  [Felipe Lube de Bragança]
- Reaproveite arquivos de capturas já realizadas. [Felipe Lube de
  Bragança]
- Nome de arquivo da captura de imagem é hash da url. [Felipe Lube de
  Bragança]
- Use os modelos do django-filer, sem modelos customizados nossos.
  [Felipe Lube de Bragança]

  BREAKING CHANGE:
  - remoção do modelo Documento (Document)
  - capturas tem associação com os arquivos (moelos do Filer)
- Ao criar uma captura, reaproveite o documento se ele já existir.
  [Felipe Lube de Bragança]
- Template padrão do filer para exibir documentos na int. admin. [Felipe
  Lube de Bragança]
- Try_task: permita exceções silenciosas. [Felipe Lube de Bragança]
- Modelo Document herdado de File (django-filer) [Felipe Lube de
  Bragança]

  BREAKING CHANGE:
  - Caminhos para arquivo serão os canônicos definidos pelo Filer
  - Campo image_capture (News) usa um novo tamanho de imagem (670x204)
  - O tipo do arquivo do documento será computado não mais por um sinal
  - Atualização dos serializers com a mudança de alguns campos
  - Simplif. de add_pdf_capture e add_fetched_image, com modelo herdado
- Refatoração de funções com uso de gerenciadores de contexto. [Felipe
  Lube de Bragança]

  - funções add_fetched_image e add_pdf_capture
  - fechamento e exclusão do arquivos temporários
  - documentação
- Integração básica com o filer para as capturas. [Felipe Lube de
  Bragança]
- Configuração incial para uso do django-filer. [Felipe Lube de
  Bragança]
- Adicione django-filer e dependências. [Felipe Lube de Bragança]

Corrigido
~~~~~~~~~
- Correção na versão dos pacotes tornado e redis, que não estão fixos.
  [Felipe Lube de Bragança]
- Fix (chore): correção na instalação do easy_thumbnails. [Felipe Lube
  de Bragança]
- Correção no pacote do celery no Pipfile. [Felipe Lube de Bragança]
- Retorne com o campo size em SimpleDocumentSerializer. [Felipe Lube de
  Bragança]
- Apague o arquivo de imagem da captura (e ela) [Felipe Lube de
  Bragança]
- Adicione a extensão no arquivo de imagem. [Felipe Lube de Bragança]
- Retorno à definição do mime_type via sinal. [Felipe Lube de Bragança]
- Propriedades adicionais do documento quando da criação da captura.
  [Felipe Lube de Bragança]
- Atualização do redis e workarround para fazer o flower funcionar.
  [Felipe Lube de Bragança]
- Refeitura de todas migrações. [Felipe Lube de Bragança]

Outros
~~~~~~
- Merge branch 'django-filer' into dev. [Felipe Lube de Bragança]
- Merge branch 'dev' into django-filer. [Felipe Lube de Bragança]
- Document: gere miniaturas necessárias à listagem dos arquivos. [Felipe
  Lube de Bragança]
- Chore: readicione o perdido django-elasticsearch-dsl. [Felipe Lube de
  Bragança]
- Revert "feat: use os modelos do django-filer, sem modelos customizados
  nossos" [Felipe Lube de Bragança]

  This reverts commit bc980135da610046e05b48d9ede46990a3dfa7e3.
- Chore: remoção de TODOS que não serão implementados mais/já foram.
  [Felipe Lube de Bragança]
- Chore: merge de dev. [Felipe Lube de Bragança]


0.6.0 (2019-03-13)
------------------

Adicionado
~~~~~~~~~~
- Feat (doc): ampliação da documentação. [Felipe Lube de Bragança]
- Lógica dos sinais mais simples com execução síncrona como failback -
  apenas um sinal para cada entidade (news e newspaper) - refatoração do
  código em funções separadas - execução síncrona se o servidor de filas
  não estiver disponível - agendamento de tarefas quando o servidor de
  filas estiver disponível - uma única verificação quanto ao servidor de
  filas - emulação do comportamento de tentativas do celery quando
  síncrono - utilização da biblioteca retrying para a emulação acima -
  qualquer erro em celery_is_avaliable deverá retornar False -
  unificação do nome da flag para indicar salvamento em sinal. [Felipe
  Lube de Bragança]
- Execute diretamente tarefas se celery não estiver disponível. [Felipe
  Lube de Bragança]

Corrigido
~~~~~~~~~
- Passe o tipo de execução para a tarefa news_set_basic_info. [Felipe
  Lube de Bragança]
- Fix (doc): fale sobre SignalException em @task_on_commit. [Felipe Lube
  de Bragança]

Outros
~~~~~~
- Merge pull request #38 from felubra/sync_failback. [Felipe Lübe de
  Bragança]

  Implementa #28
- Chore: atualização do changelog. [Felipe Lube de Bragança]


0.5.1 (2019-03-11)
------------------

Corrigido
~~~~~~~~~
- Atualização de segurança do django (2.1.7) [Felipe Lube de Bragança]

Outros
~~~~~~
- Chore: atualização do changelog. [Felipe Lube de Bragança]


0.5.0 (2019-03-11)
------------------

Adicionado
~~~~~~~~~~
- (page) nomes em português para o app e modelos. [Felipe Lube de
  Bragança]
- Campo teaser (page) com formatação rica. [Felipe Lube de Bragança]
- Endpoints da api para obter páginas e conjuntos de páginas comuns.
  [Felipe Lube de Bragança]
- Campo para mostrar ou não um link para a página no menu principal.
  [Felipe Lube de Bragança]
- Substituição do django-bower pelo django-npm. [Felipe Lube de
  Bragança]
- Substituição do django-bower pelo django-npm. [Felipe Lube de
  Bragança]
- Botão maximizar no editor. [Felipe Lube de Bragança]
- Botão para maximizar o editor. [Felipe Lube de Bragança]
- Defina uma altura mínima para o editor. [Felipe Lube de Bragança]
- Defina a barra de ferramentas e os formatos do editor. [Felipe Lube de
  Bragança]
- Utilize o formato json para definir o toolbar. [Felipe Lube de
  Bragança]
- Adicione a possibilidade de configurar os formatos. [Felipe Lube de
  Bragança]
- Adicione uma borda vermelha para o campo com erro. [Felipe Lube de
  Bragança]
- Use uma mensagem de erro em inglês que poderá ser traduzida. [Felipe
  Lube de Bragança]
- Utilize o validador de texto em html. [Felipe Lube de Bragança]
- Testes para o validador. [Felipe Lube de Bragança]
- Um validador simples para html sem conteúdo. [Felipe Lube de Bragança]
- Adicione beautifulsoup4, usando para validar HTML. [Felipe Lube de
  Bragança]
- Use o widget do editor quilljs. [Felipe Lube de Bragança]
- Atributos personalizados para controlar o editor; revisão código.
  [Felipe Lube de Bragança]
- Assets necessários para o widget funcionar dentro do próprio app.
  [Felipe Lube de Bragança]
- Implementação inicial do widget e util. em Notícia. [Felipe Lube de
  Bragança]
- Página: modelos e estruturas de admin. básicas. [Felipe Lube de
  Bragança]
- Adicione application/zip à lista de mimes suportados. [Felipe Lube de
  Bragança]
- Serializer simples para apenas o essencial sobre um documento. [Felipe
  Lube de Bragança]
- Suporte para thumbnails de documentos pela api. [Felipe Lube de
  Bragança]
- Reutilize uma propriedad usada pelo elastic_search na api. [Felipe
  Lube de Bragança]
- Feat (api): adicione campos com as capturas de página (imagem e pdf)
  [Felipe Lube de Bragança]
- Suporte ao CORS: em dev libere tudo. [Felipe Lube de Bragança]
- Endpoints para a api para documentos e notícias. [Felipe Lube de
  Bragança]
- News: indexe o ano de publicação num campo próprio. [Felipe Lube de
  Bragança]
- Suporte ao CORS: em dev libere tudo. [Felipe Lube de Bragança]
- Endpoints para a api para documentos e notícias. [Felipe Lube de
  Bragança]
- Não indexe certos ampos. [Felipe Lube de Bragança]
- Analisadores da língua portuguesa na indexação. [Felipe Lube de
  Bragança]
- Tente novamente em caso de execção ConnectionError. [Felipe Lube de
  Bragança]
- Torne o campo body de news nullable. [Felipe Lube de Bragança]
- Exceção ValueError se a análise do fetcher falhar. [Felipe Lube de
  Bragança]
- Script para baixar recursos necessários para o nltk funcionar. [Felipe
  Lube de Bragança]
- Versão 0.4.0. [Felipe Lube de Bragança]
- Torne a geração de capturas uma transação atômica. [Felipe Lube de
  Bragança]

Corrigido
~~~~~~~~~
- Remoção de cores duplicadas na toolbar do editor. [Felipe Lube de
  Bragança]
- Defina as cores do editor numa variável para melhor legibilidade.
  [Felipe Lube de Bragança]
- Detecte a mudança para a tela cheia corretamente. [Felipe Lube de
  Bragança]
- Adicione os arquivos screenfull aos arquivos estáticos. [Felipe Lube
  de Bragança]
- Atualização do pipfile. [Felipe Lube de Bragança]
- Altere a ordem dos métodos. [Felipe Lube de Bragança]
- Remova o editor quill do formulário de notícias. [Felipe Lube de
  Bragança]
- Atualização no placeholder e definição dos botões da barra. [Felipe
  Lube de Bragança]
- Saída de atributos personalizados no template. [Felipe Lube de
  Bragança]
- String vazia ao invés de 'None' se o campo estiver em branco. [Felipe
  Lube de Bragança]
- Inclusão do campo url em NewspaperSerializer. [Felipe Lube de
  Bragança]
- Englobe blocos de captura em transações. [Felipe Lube de Bragança]
- Corrija a busca por uma palavra-chave existente. [Felipe Lube de
  Bragança]
- Trabalhos duplicados para news quando estiver salvando um jornal.
  [Felipe Lube de Bragança]
- Atencipe a possibilidade de OSError pela ferramenta wkhtmltopdf.
  [Felipe Lube de Bragança]

Outros
~~~~~~
- Merge branch 'page_app' into dev. [Felipe Lube de Bragança]
- Chore: atualização do package.json. [Felipe Lube de Bragança]
- Style: variáveis legíveis para configurações do editor. [Felipe Lube
  de Bragança]
- Chore: merge from elastic_search. [Felipe Lube de Bragança]
- Merge branch 'quill_widget' into page_app. [Felipe Lube de Bragança]
- Revert "feat: botão para maximizar o editor" [Felipe Lube de Bragança]

  This reverts commit b0cbf85eb2371704f6c59b0feb43a08055bd5cf7.
- Merge branch 'quill_widget' into page_app. [Felipe Lube de Bragança]
- Merge branch 'quill_widget' into page_app. [Felipe Lube de Bragança]
- Merge branch 'quill_widget' into page_app. [Felipe Lube de Bragança]
- Merge branch 'quill_widget' into page_app. [Felipe Lube de Bragança]
- Merge branch 'quill_widget' into page_app. [Felipe Lube de Bragança]
- Merge branch 'quill_widget' into page_app. [Felipe Lube de Bragança]
- Merge branch 'quill_widget' into page_app. [Felipe Lube de Bragança]
- Merge branch 'public_api' into elastic_search. [Felipe Lube de
  Bragança]
- Chore: merge from public_api. [Felipe Lube de Bragança]
- Merge branch 'public_api' into elastic_search. [Felipe Lube de
  Bragança]
- Merge branch 'public_api' into elastic_search. [Felipe Lube de
  Bragança]
- Merge de origin/dev. [Felipe Lube de Bragança]


0.4.0 (2019-02-25)
------------------

Adicionado
~~~~~~~~~~
- Versão 0.4.0. [Felipe Lube de Bragança]
- + gitchangelog para fazer o changelog automaticamente. [Felipe Lube de
  Bragança]
- Englobe certas operações numa transação. [Felipe Lube de Bragança]
- Associe, de uma vez só, várias palavras-chave a uma notícia. [Felipe
  Lube de Bragança]
- Add_news_task: faça as capturas adicionais. [Felipe Lube de Bragança]
- [wip] campo imagem no formulário administrativo. [Felipe Lube de
  Bragança]
- Tarefa news_add_pdf_capture agendada via sinal. [Felipe Lube de
  Bragança]
- Agende a execução do job para versão arquivada. [Felipe Lube de
  Bragança]
- Tarefa news_set_basic_info agendada via sinal. [Felipe Lube de
  Bragança]
- [wip] simplificação: salve jornal via sinais. [Felipe Lube de
  Bragança]
- Todo. [Felipe Lube de Bragança]
- Modelo para o jornal/veículo da notícia; fix: add_additional_info.
  [Felipe Lube de Bragança]
- Celery compatível com python 3.6+; flower p/ monitoramento. [Felipe
  Lube de Bragança]
- Indexe o thumbnail da notícia ao invés do objeto de captura - adicione
  um alias 'thumbnail' para imagens 250x250px - adicione uma prop para
  pegar a url da imagem gerada - indexe a url da imagem. [Felipe Lube de
  Bragança]
- Não verifique pelo servidor de filas em desenvolvimento. [Felipe Lube
  de Bragança]
- É possível agendar tarefas com o celery antes de iniciar o app?
  [Felipe Lube de Bragança]
- Não indexe artefatos do tipo documento. [Felipe Lube de Bragança]
- Atualização do pipfile.lock. [Felipe Lube de Bragança]
- Paz na guerra de dependências. [Felipe Lube de Bragança]
- Torne a geração de capturas uma transação atômica. [Felipe Lube de
  Bragança]
- Decorador de log mais consiso. [Felipe Lube de Bragança]
- Simplifique o processo de salvamento da notícia com agendamentos.
  [Felipe Lube de Bragança]
- Atualização do popfile. [Felipe Lube de Bragança]
- Utilize a versão do gitub do celery, que suporta python 3.6+ [Felipe
  Lube de Bragança]
- Ignore data de publicação fora do padrão que Fetcher trouxer. [Felipe
  Lube de Bragança]
- Tente novamente as tarefas que dão erro de bloqueio no sqlite. [Felipe
  Lube de Bragança]
- Celery compatível com python 3.6+; flower p/ monitoramento. [Felipe
  Lube de Bragança]
- Dê um nome humano para as capturas. [Felipe Lube de Bragança]
- Feat(index): adicione informações sobre as capturas. [Felipe Lube de
  Bragança]
- Se uma notícia for aapagada, apague suas capturas. [Felipe Lube de
  Bragança]
- Alterações nos modelos relacionados de news - salve-os automaticmanete
  pela config do índice - inclua mais detalhes sobre os itens de
  taxonomia. [Felipe Lube de Bragança]
- Adicione o redis. [Felipe Lube de Bragança]
- Adicione o flower para monitorar tarefas do celery. [Felipe Lube de
  Bragança]
- Indexação: News: inclusão de campos de Traceable(Editorial)Model.
  [Felipe Lube de Bragança]
- Indexação de documentos. [Felipe Lube de Bragança]
- Indexação do modelo Notícia. [Felipe Lube de Bragança]
- Adicione um campo reverso para o relacionamento. [Felipe Lube de
  Bragança]
- Adicione as bibliotecas usadas para int. com o ElasticSearch. [Felipe
  Lube de Bragança]
- Decorador de log mais consiso. [Felipe Lube de Bragança]
- Simplifique o processo de salvamento da notícia com agendamentos.
  [Felipe Lube de Bragança]
- Atualização do popfile. [Felipe Lube de Bragança]
- Utilize a versão do gitub do celery, que suporta python 3.6+ [Felipe
  Lube de Bragança]
- Ignore data de publicação fora do padrão que Fetcher trouxer. [Felipe
  Lube de Bragança]
- Tente novamente as tarefas que dão erro de bloqueio no sqlite. [Felipe
  Lube de Bragança]
- Celery compatível com python 3.6+; flower p/ monitoramento. [Felipe
  Lube de Bragança]
- Npm script para rodar o celery no windows. [Felipe Lube de Bragança]
- Logue a inserção múltipla de notícias. [Felipe Lube de Bragança]
- Tarefas para inserir uma imagem e palavras-chave para notícia. [Felipe
  Lube de Bragança]
- Simplificação na chamada às tarefas no método save de news -
  parâmetros nas tarefas para controlar melhor o uso de recursos -
  execução paralela de tarefas - retorno das tarefas. [Felipe Lube de
  Bragança]
- Divida a execução da tarefa de inserção em grupos de 5. [Felipe Lube
  de Bragança]
- Botão para inserir múltimas notícias na interface administrativa.
  [Felipe Lube de Bragança]
- Formulário básico para inserção de urls. [Felipe Lube de Bragança]
- Somente adicione uma imagem à notícia que não tiver nenhuma. [Felipe
  Lube de Bragança]
- Simplifique a assnatura de add_additional_info. [Felipe Lube de
  Bragança]
- Logger: failback para usuário que modificou por último o objeto.
  [Felipe Lube de Bragança]
- Remova django_rq, dependências e configurações. [Felipe Lube de
  Bragança]
- Poc do celery como queue backend. [Felipe Lube de Bragança]
- Adicione o pacote celery. [Felipe Lube de Bragança]
- Utilize um job para adicionar informações extra a notícia. [Felipe
  Lube de Bragança]
- Verifique apenas se a notícia tem um título antes de salvá-la. [Felipe
  Lube de Bragança]
- Newsfetcher: função p/ pegar o título de uma notícia da web. [Felipe
  Lube de Bragança]
- Substituição do django-bower pelo django-npm. [Felipe Lube de
  Bragança]
- Permita a não busca de imagens usando o goose. [Felipe Lube de
  Bragança]
- Manage.py executável. [Felipe Lube de Bragança]
- Mova a pasta 'lib' para o nível superior. [Felipe Lube de Bragança]
- Organização do módulo file_previews. [Felipe Lube de Bragança]
- Gerador failback que retorna um ícone. [Felipe Lube de Bragança]
- Acerte a ordem de THUMBNAIL_SOURCE_GENERATORS. [Felipe Lube de
  Bragança]
- Novo projeto file-icon-vectors para ícones. [Felipe Lube de Bragança]
- Adicione cairosvg para converter arquivos svg. [Felipe Lube de
  Bragança]
- Melhorias no dicionário de palavras vazias. [Felipe Lube de Bragança]

  - abra o dicionário de um projeto instalado pelo bower
  - em caso de erro, retorne um dicionário vazio
  - adicione o projeto 'stopwords-iso'
- Gerenciamento de dependências com bower. [Felipe Lube de Bragança]
- Melhor geração de visualizações pdf. [Felipe Lube de Bragança]

  - gere a visualizações num diretório temporário
  - use apenas o arquivo da primeira página como fonte para a miniatura
  - apague arquivos temporários gerados
- Faça o downgrade do django para permitir debug. [Felipe Lube de
  Bragança]
- Pré-visualização de arquivos de documentos. [Felipe Lube de Bragança]
- Teste para a nova funcionalidade stopword. [Felipe Lube de Bragança]
- Ignore uma palavra vazia como palavra-chave. [Felipe Lube de Bragança]
- Adicione o campo idioma para Notícia. [Felipe Lube de Bragança]
- Feat(docker): instale o corpora para funcionamento de nlp;
  organização. [Felipe Lube de Bragança]
- Doker-compose para web e arquivos. [Felipe Lube de Bragança]
- Adicione .dockerignore. [Felipe Lube de Bragança]
- Instalação do wkhtmltopdf; exposição da porta. [Felipe Lube de
  Bragança]
- Alteração das configuração para homologação. [Felipe Lube de Bragança]
- Dockerfile inicial. [Felipe Lube de Bragança]

Corrigido
~~~~~~~~~
- Correta execução de operações que poderão falhar. [Felipe Lube de
  Bragança]
- Correta utilização do lambda. [Felipe Lube de Bragança]
- Correções na captura de imagem da notícia - podem haver várias
  capturas de imagem com a mesma url, mas notícias diferentes. [Felipe
  Lube de Bragança]
- Representação de capturas em string safa. [Felipe Lube de Bragança]
- Remoção de código obsoleto. [Felipe Lube de Bragança]
- Newspaper: agende o trabalho após o commit; evite loops infinitos.
  [Felipe Lube de Bragança]
- Simplificação de add_fetched_keywords com objeto Q. [Felipe Lube de
  Bragança]
- Alterações na indexação de capturas em pdf. [Felipe Lube de Bragança]
- Mais robustez na propriedade image_capture_indexing. [Felipe Lube de
  Bragança]
- Indexe a url da notícia. [Felipe Lube de Bragança]
- Agende corretamente as tarefas num grupo paralelo. [Felipe Lube de
  Bragança]
- Correção na verificação do título no formulário administrativo.
  [Felipe Lube de Bragança]
- Atualização do piplock. [Felipe Lube de Bragança]
- Atualização do pipfile.lock. [Felipe Lube de Bragança]
- Persistência correta da data de publicação no Fetcher. [Felipe Lube de
  Bragança]
- Falhas de acesso ao servidor de filas devem ser críticas. [Felipe Lube
  de Bragança]
- Inclusão da variável err. [Felipe Lube de Bragança]
- Correção na chamada de add_image_for_news. [Felipe Lube de Bragança]
- Atualização do pipfile.lock. [Felipe Lube de Bragança]
- Inclusão da variável err. [Felipe Lube de Bragança]
- Correção na chamada de add_image_for_news. [Felipe Lube de Bragança]
- Utilize o ip ao invés de localhost. [Felipe Lube de Bragança]
- Renomeie funções de tarefa com o sufixo _task. [Felipe Lube de
  Bragança]
- Remoção de condição desnecessária. [Felipe Lube de Bragança]
- Fix #22: Somente chame tasks do celery usando o on_commit. [Felipe
  Lube de Bragança]
- Fix #19: Botões de ação fixos na interface administrativa. [Felipe
  Lube de Bragança]
- Simplificação de chamada à super() [Felipe Lube de Bragança]
- Atualização do nome das classes. [Felipe Lube de Bragança]
- Não busque imagens para não atrapalhar o mock. [Felipe Lube de
  Bragança]
- Utilize o idioma do artigo para buscar stopwords. [Felipe Lube de
  Bragança]
- Fix #11: nomes de arquivo url friendly e com prefixo correto. [Felipe
  Lube de Bragança]
- Fix #11: nomes de arquivo url friendly e com prefixo correto. [Felipe
  Lube de Bragança]
- Fieldsets padrão em formulários administrativos. [Felipe Lube de
  Bragança]
- Mostre os campos de taxonomia corretamente para documento. [Felipe
  Lube de Bragança]
- Otimizações para uso de memória. [Felipe Lube de Bragança]
- Configuração para proxy reverso. [Felipe Lube de Bragança]
- Restaure 'debug_toolbar' app em desenvolvimento. [Felipe Lube de
  Bragança]
- Restaure uma configuração dos templates. [Felipe Lube de Bragança]
- Correção na instalação de dep wkhtmltopdf. [Felipe Lube de Bragança]

Outros
~~~~~~
- Merge de elastic_search. [Felipe Lube de Bragança]
- Merge branch 'dev' into elastic_search. [Felipe Lube de Bragança]
- Merge de dev. [Felipe Lube de Bragança]
- Merge pull request #27 from felubra/news_bulk_insertion. [Felipe Lübe
  de Bragança]

  Permita a inserção de múltiplas notícias de uma vez só.
- Tarefa para adicionar múltiplas notícias via url. [Felipe Lube de
  Bragança]
- Merge pull request #23 from felubra/delayed_jobs__celery. [Felipe Lübe
  de Bragança]

  Substitua o Django_rq pelo celery para fazer tarefas em segundo plano
- Merge pull request #18 from felubra/files_thumbnail. [Felipe Lübe de
  Bragança]

  Visualizações para arquivo
- Ignore components instalados pelo bower. [Felipe Lube de Bragança]
- Revert "feat: faça o downgrade do django para permitir debug" [Felipe
  Lube de Bragança]

  This reverts commit 8612f3c2837373d81c7ecffeb05d925b3aefe504.
- Ignore a pasta usada pelo virtualenv. [Felipe Lube de Bragança]
- Revert "fix #11: nomes de arquivo url friendly e com prefixo correto"
  [Felipe Lube de Bragança]

  This reverts commit 16d54697c986943bfb76a50e8766dbcb6c58a262.
- Merge branch 'master' into dev. [Felipe Lube de Bragança]
- Merge pull request #14 from felubra/homologacao. [Felipe Lübe de
  Bragança]

  Configuração básica para a hospedagem no container docker
- Remoção do debug toolbar em todos ambientes. [Felipe Lube de Bragança]


0.3.0 (2019-01-23)
------------------

Adicionado
~~~~~~~~~~
- Fieldsets para Documento. [Felipe Lube de Bragança]
- Merge com 'documents_simplify' [Felipe Lube de Bragança]

  As modificações de 'documents_simplify' tocam na interface
  administrativa
- Tradução das mensagens em FileValidator, documentação. [Felipe Lube de
  Bragança]
- Obsoleta PDFDocument e ImageDocument. [Felipe Lube de Bragança]

  BREAKING CHANGE:
  - Somente uma classe para lidar com arquivos-documento: Document
  - O  destino do arquivo do Documento é determinado pelo seu mimetype
  - Refeitura das migrações
- Adicione validador para arquivos. [Felipe Lube de Bragança]
- Tom de cor vermelho para interface administrativa. [Felipe Lube de
  Bragança]
- Defina um site administrativo customizado. [Felipe Lube de Bragança]
- Altere a linguagem do django para pt-br. [Felipe Lube de Bragança]

Corrigido
~~~~~~~~~
- Corrija a execução do job para buscar pdfs. [Felipe Lube de Bragança]
- Acerto na cor do breadcrumb. [Felipe Lube de Bragança]
- Remoção do vermelho excessivo; novas regras. [Felipe Lube de Bragança]
- Remoção de código não usado. [Felipe Lube de Bragança]
- Correção em nome de variável em FileValidator. [Felipe Lube de
  Bragança]
- Remoção do validador no formulário, pois já funciona no modelo.
  [Felipe Lube de Bragança]

Outros
~~~~~~
- Revert "Revert "Atualização do Django 2.1.2 => 2.1.5"" [Felipe Lube de
  Bragança]

  This reverts commit a35db69133e07c4e6754d75501b2819d363228b4.
- Merge branch 'master' into admin_rebranding. [Felipe Lube de Bragança]
- Revert "Atualização do Django 2.1.2 => 2.1.5" [Felipe Lube de
  Bragança]

  This reverts commit 6b3368559bdb21174a302421c0087b1ac463bd17.


0.2.1 (2019-01-21)
------------------

Outros
~~~~~~
- Atualização do Django 2.1.2 => 2.1.5. [Felipe Lube de Bragança]


0.2.0 (2019-01-21)
------------------

Adicionado
~~~~~~~~~~
- Feat(doc): Documentação de NewsFetcher. [Felipe Lube de Bragança]
- Feat(doc): documentação dos recebedores de sinal. [Felipe Lube de
  Bragança]
- Feat(doc): documentação de modelos administrativos e formulários.
  [Felipe Lube de Bragança]
- Feat(doc): melhor documentação dos modelos e remoção de código não
  usado. [Felipe Lube de Bragança]
- TraceableAdminModel: disponibilize COMMON_FIELDSETS p/ filhos. [Felipe
  Lube de Bragança]
- Documents: remoção e atualização de campos; simplificação BREAKING
  CHANGE: - pdf_file e image_file renomeados para file - sempre tente
  determinar o mimetype do documento quando possível. [Felipe Lube de
  Bragança]
- Reorganização dos arquivos seção admin; validação de uploads. [Felipe
  Lube de Bragança]
- Geração segura de slugs. [Felipe Lube de Bragança]
- Reorganização do código em módulos separados. [Felipe Lube de
  Bragança]
- Remoção do app news_fetcher. [Felipe Lube de Bragança]
- Capture a imagem da notícia como uma imagem do acervo. [Felipe Lube de
  Bragança]

  BREAKING CHANGE:
  - Novos modelos ImageDocument e NewsImageCapture
  - Remoção do campo image em News
  - alteração de has_basic_info
  - novos fetch_image() e add_fetched_image
  - Novos itens de administração DocumentAdmin e ImageDocumentAdmin
  - Remoção do campo imagem de NewsAdmin
  - Refeitura de todas migrações
- Subclasses de Document guardarão o arquivo. [Felipe Lube de Bragança]
- Permita acesso direto aos arquivos enviados. [Felipe Lube de Bragança]
- Definição de MEDIA_ROOT e novas constantes. [Felipe Lube de Bragança]
- Substituição dos apps ArchivedNews e Documents. [Felipe Lube de
  Bragança]

  BREAKING CHANGE:
  News/ArchivedNews:
  - campos `title`, `teaser`, `keywords` e `slug` herdados de Artifact
  - remoção do campo `status` e constantes associadas
  - status de publicação herdados da classe TraceableEditorialModel
  - campo `url` é  obrigatório
  - remoção das flags de processamento
  - remoção do campo `images`
  - substituição do campo `text` por `body`
  - substituição do campo `summary` por `teaser`
  - migração da lógica do negócio para o modelo News
  - `has_basic_info` simplificado
  - remoção de `needs_reprocessing`, `has_web_archive_url` e `has_error`
  - remoção de is_new, is_queued, is_processed, is_published, has_web_archive_url,
  needs_reprocessing, has_error, force_pdf_capture, force_archive_org_processing, force_basic_processing

  Logger:
  - Substituição da arquitetura de sinais pela invocação direta do log, através de um decorador

  Taxonomy:
  - Criação de TaxonomyItem, classe padrão para itens de taxonomia
  - Criação de Subject e Keyword

  Modelos novos:
  Artifact, Document, PDFDocument, NewsPDFCapture e News

  Configuração do django para usar os modelos novos
- TraceableEditorialModel modelo para um fluxo editorial básico. [Felipe
  Lube de Bragança]
- Remoção de constantes, alteração em NEWS_FETCHER_SAVED_DIR_PDF.
  [Felipe Lube de Bragança]
- Use o middleware para determinar o usuário atual. [Felipe Lube de
  Bragança]
- Adição de fieldsets padrão para TraceableAdminModel. [Felipe Lube de
  Bragança]
- Documentação dos campos de TraceableModel. [Felipe Lube de Bragança]
- Coloque o nome do usuário na mensagem de log; correções diversas.
  [Felipe Lube de Bragança]
- Adicione o django-currentuser para pegar o usuário atual. [Felipe Lube
  de Bragança]
- Início de um decorador para logging básico. [Felipe Lube de Bragança]

Corrigido
~~~~~~~~~
- Correção em docstring dos testes e reativação de suíte esquecida.
  [Felipe Lube de Bragança]
- Teaser em branco para artifact; migrações dos commits anteriores.
  [Felipe Lube de Bragança]
- Relacione o nome do usuário criador e modificador com o da notícia.
  [Felipe Lube de Bragança]
- Utilize sinais para determinar o tipo e tamanho dos documentos.
  [Felipe Lube de Bragança]
- Lógica melhor para salvar tipo e tamanho do arquivo; alterações.
  [Felipe Lube de Bragança]

  BREAKING CHANGE:
  - Document.filesize agora é charfield
  - DocumentAdminModelBase para lidar com a lógica do tamanho e do tipo
- Não permita a criação de notícia sem url, valide a url. [Felipe Lube
  de Bragança]
- Não permita a criação de um artefato sem título. [Felipe Lube de
  Bragança]
- File_hash não deve aparecer na interface administrativa. [Felipe Lube
  de Bragança]
- Log_process: retorne o valor da função em caso de êxito. [Felipe Lube
  de Bragança]

Outros
~~~~~~
- Merge pull request #7 from felubra/artifact_app. [Felipe Lübe de
  Bragança]

  Reestruturação dos aplicativos para Notícia, Documento e Taxonomia
- Testes preliminares. [Felipe Lube de Bragança]
- Doc: mudança na nomenclatura dos itens de auditoria. [Felipe Lube de
  Bragança]
- Adicione o módulo magic para detectar tipos de arquivo. [Felipe Lube
  de Bragança]
- Doc: retorno e expansão de `documento` ao invés de `arquivo do
  usuário` [Felipe Lube de Bragança]
- Use a biblioteca loguru para logar mensagens. [Felipe Lube de
  Bragança]
- Adicione a biblioteca loguru para simplificar o processo de log.
  [Felipe Lube de Bragança]
- Mudança em nome de variável `job_signals` => `process_signals` [Felipe
  Lube de Bragança]
- Rascunho para requisitos sem local definido ainda. [Felipe Lube de
  Bragança]
- Organização e expansão dos requisitos. [Felipe Lube de Bragança]
- Mude 'Site da notícia' para 'Veículo da notícia' [Felipe Lube de
  Bragança]
- Novo app para logs e correções no carregamento síncrono de info.
  [Felipe Lube de Bragança]
- Todo. [Felipe Lube de Bragança]
- Não logue nada, utilize sinais para com. com o app Logger. [Felipe
  Lube de Bragança]
- Defina sinais para indicar status de início, sucesso e falha dos jobs.
  [Felipe Lube de Bragança]
- Capture tempos de operação dos outros jobs também. [Felipe Lube de
  Bragança]
- Restrinja atualização dos campos e somente se houver informações.
  [Felipe Lube de Bragança]
- Aplicativo Logger - Concentra a escritura de logs para STDOUT com base
  em sinais enviados por outros apps - Loga jobs para obtenção
  automática de informações e capturas. [Felipe Lube de Bragança]
- Nome correto para arquivo que apenas recebe sinais. [Felipe Lube de
  Bragança]
- Utilize '_keywords' apenas onde quando for necessário. [Felipe Lube de
  Bragança]
- Refatoração de get_fieldsets() [Felipe Lube de Bragança]
- Refatoração de `process_news` e novas funções - Refatoração de
  `process_news` com utilização de funções dedicadas - Lógica mais
  robusta com `_merge_extractions` para o mesclar objetos de bibliotecas
  diferentes - Documentação das funções. [Felipe Lube de Bragança]
- Faça operações sincronicamente se o redis não estiver disponível.
  [Felipe Lube de Bragança]
- Operações diretas se o redis não estiver disponível para executar
  jobs. [Felipe Lube de Bragança]
- Renomeie a string '@todo' por 'TODO:' para maior destaque. [Felipe
  Lube de Bragança]
- Mostre o novo campo published_date no form administrativo. [Felipe
  Lube de Bragança]
- Defina o timezone padrão do site para São Paulo. [Felipe Lube de
  Bragança]
- Biblioteca goose3 para pegar mais informações e como failback. [Felipe
  Lube de Bragança]
- Adicione o campo published_date. [Felipe Lube de Bragança]
- Atualização do changelog. [Felipe Lube de Bragança]
- Atualização do changelog, seção auditoria. [Felipe Lube de Bragança]
- Alterações na parte administrativa para Notícia Arquivada - Link para
  a notícia no título - Classe com método comum de salvamento de modelos
  `TraceableModel` [Felipe Lube de Bragança]
- Renomeação de arquivo. [Felipe Lube de Bragança]
- Reorganização do changelog e adição de requisito. [Felipe Lube de
  Bragança]
- Pequenas refatoração e documentação. [Felipe Lube de Bragança]
- ArchivedNews: renomeado has_web_archive => has_web_archive_url.
  [Felipe Lube de Bragança]


0.1.0 (2018-12-19)
------------------

Outros
~~~~~~
- Atualização do changelog - versão 0.1.0 publicada. [Felipe Lube de
  Bragança]
- Atualização nos testes - reutilize self.client - faça login no começo
  do teste - término de test_fields_for_existing_item - utilize uma
  resposta real em test_fields_for_new_item. [Felipe Lube de Bragança]
- Remova inteiramente o campo insertion_mode no modo de edição. [Felipe
  Lube de Bragança]
- Alteração na mensagem de log. [Felipe Lube de Bragança]
- Interface adminstrativa básica para os modelos do tipo documento.
  [Felipe Lube de Bragança]
- Remova todo que não será implementado. [Felipe Lube de Bragança]
- Atualização do changelog. [Felipe Lube de Bragança]
- Deixe os títulos em maiúsculo para facilitar a leitura. [Felipe Lube
  de Bragança]
- Sem url única para permitir várias capturas por notícia. [Felipe Lube
  de Bragança]
- Atualização e organização do changelog. [Felipe Lube de Bragança]
- Adicione pylint-django. [Felipe Lube de Bragança]
- Mudança no estilo do formulário inline do documento de captura.
  [Felipe Lube de Bragança]
- Faça o campo da url do documento de  captura não editável. [Felipe
  Lube de Bragança]
- Importação de dependências que estavam faltando. [Felipe Lube de
  Bragança]
- Atualização dos testes para evitar exceção de transação. [Felipe Lube
  de Bragança]
- Novo app para documentos - transforme as imagens capturadas para a
  notícia arquivada em instâncias do tipo de conteúdo do tipo documento
  - migrações para esta alteração a taxonomia - atualização do fetcher
  para criar o documento. [Felipe Lube de Bragança]
- ArchivedNews: reorganização dos arquivos do admin. [Felipe Lube de
  Bragança]
- Reorganização: app de taxonomia dedicado. [Felipe Lube de Bragança]
- Alteração de requisitos - toda mídia é documento. [Felipe Lube de
  Bragança]
- Anotações de tipo. [Felipe Lube de Bragança]
- Atualização dos requisitos de pesquisa. [Felipe Lube de Bragança]
- Novos requisitos de mudança. [Felipe Lube de Bragança]


0.0.0 (2018-12-13)
------------------

Outros
~~~~~~
- Versão 0.0.0. [Felipe Lube de Bragança]
- Remova bloco duplicado de texto. [Felipe Lube de Bragança]
- Merge branch 'log-entry-actions' [Felipe Lube de Bragança]
- Migrações. [Felipe Lube de Bragança]
- Log de modificações das entidades nos jobs. [Felipe Lube de Bragança]
- Informação LogEntry para uma palavra-chave criada indiretamente.
  [Felipe Lube de Bragança]
- Mais informações de auditoria nos modelos: usuários e timestamps.
  [Felipe Lube de Bragança]
- Evite erros de atomicidade ao entrar no contexto transaction.atomic.
  [Felipe Lube de Bragança]
- Inclusão de objetivos no changelog. [Felipe Lube de Bragança]
- Testes com o formulário administrativo para ArchivedNews - Verifique
  que o nosso campo virtual 'insertion_mode' está no form - [WIP] teste
  a presença de campos quando editando. [Felipe Lube de Bragança]
- Ignore arquivos estáticos coletados pelo Django. [Felipe Lube de
  Bragança]
- Teste se o modelo Keyword define corretamente o campo slug após save()
  [Felipe Lube de Bragança]
- Evite uma exceção ValueError quando verificando has_basic_info.
  [Felipe Lube de Bragança]
- Adicione teste para o estado inicial das flags do modelo ArchivedNews.
  [Felipe Lube de Bragança]
- Organização dos requisitos e do changelog. [Felipe Lube de Bragança]
- 'squash' nas migrações. [Felipe Lube de Bragança]
- Se não houver conexão disponivel com o redis, altere o status da
  notícia. [Felipe Lube de Bragança]
- Novo status para quando não há serviço de fila disponível. [Felipe
  Lube de Bragança]
- Refatoração. [Felipe Lube de Bragança]
- Atualização de requisitos. [Felipe Lube de Bragança]
- Adicionados rope e redis. [Felipe Lube de Bragança]
- Não verifique se o modelo é novo, apenas se precisa de processamento.
  [Felipe Lube de Bragança]
- Alteração nos nomes e nas descrições dos campos do modelo
  ArchivedNews. [Felipe Lube de Bragança]
- Remoção do campo manual_insertion. [Felipe Lube de Bragança]
- Refatoração do formulário administrativo para Notícias Arquivadas -
  Inclusão de um campo não persistido insertion_mode - Texto de ajuda
  das flags de acordo com a operção criar/editar - Ajuste na lógica para
  verificar edição manual. [Felipe Lube de Bragança]
- 'squash' nas migrações. [Felipe Lube de Bragança]
- Novo requisito. [Felipe Lube de Bragança]
- Só execute os jobs se o conteúdo é novo ou se forçado; novo job.
  [Felipe Lube de Bragança]
- Ao final do processo, limpe a flag para forçar a execução do job.
  [Felipe Lube de Bragança]
- Nova funcionalidade para pegar a URL do Internet Archive, se houver.
  [Felipe Lube de Bragança]
- Novas propriedades para indicar a presença de informações. [Felipe
  Lube de Bragança]
- Alterações nos campos. [Felipe Lube de Bragança]
- Novos campos na interface administrativa. [Felipe Lube de Bragança]
- Refatoração em clean() com verificação de urls - Pegue corretamente a
  flag manual_insertion - Exija pelo menos uma url. [Felipe Lube de
  Bragança]
- Novos status, campos e propriedades - Flags para forçar o
  reprocessamento da notícia - Propriedade para indicar que o
  reprocessamento é necessário - Campo url pode ser nulo - Novo campo da
  URL da notícia no Internet Archive - Novo status para notícia com
  arquivo no Internet Archive. [Felipe Lube de Bragança]
- Configuração correta dos paths. [Felipe Lube de Bragança]
- Adicione a biblioteca requests. [Felipe Lube de Bragança]
- Ignore aquivos de configuração do pyCharm. [Felipe Lube de Bragança]
- Documentação. [Felipe Lube de Bragança]
- Validação especial do título em caso de inserção manual. [Felipe Lube
  de Bragança]
- Defina as palavras-chave extraídas pelo fetcher num campo protegido.
  [Felipe Lube de Bragança]
- Melhor fluxograma com uso do método save_related - Migre operações do
  Model.save para ModelAdmin.save_related - Crie e inclua instâncias de
  palavas-chave extraídas pelo fetcher - Migrações para utilizar o
  modelo para palavras-chave. [Felipe Lube de Bragança]
- Modelo para palavras-chave. [Felipe Lube de Bragança]
- Adicionado pdir2 às dependências de desenvolvimento. [Felipe Lube de
  Bragança]
- Adição de requisitos de usuário. [Felipe Lube de Bragança]
- Organização do formulário. [Felipe Lube de Bragança]
- Documentação básica do modelo. [Felipe Lube de Bragança]
- Utilize um nome melhor para flag, não processe se for uma in. manual.
  [Felipe Lube de Bragança]
- Utilize a nova constante com o local da pasta de salvamento. [Felipe
  Lube de Bragança]
- Novas configurações para os locais de salvamento da notícia. [Felipe
  Lube de Bragança]
- Permita a inserção manual dos dados da notícia. [Felipe Lube de
  Bragança]
- Não exiba campos desnecessários na interface administrativa. [Felipe
  Lube de Bragança]
- Exclua o diretório media. [Felipe Lube de Bragança]
- Adicionado campo que faltava. [Felipe Lube de Bragança]
- Coloque as msgs de log para início do processo nos jobs. [Felipe Lube
  de Bragança]
- Utilize as flags ao invés de verificar o status diretamente. [Felipe
  Lube de Bragança]
- Refatoração: mais robustez e definção de status intermediários.
  [Felipe Lube de Bragança]
- Algumas flags de status e label para o modelo Archived News. [Felipe
  Lube de Bragança]
- Utilize a uma versão não liberada ainda do pdfkit. [Felipe Lube de
  Bragança]
- Atualização de requisitos. [Felipe Lube de Bragança]
- Correção de status. [Felipe Lube de Bragança]
- Alteração nos status. [Felipe Lube de Bragança]
- Adicione meta informações ao modelo Archived News. [Felipe Lube de
  Bragança]
- Processe a notícia que estiver com erro e evite loops infinitos.
  [Felipe Lube de Bragança]
- Ignore a pasta onde são salvas as notícias. [Felipe Lube de Bragança]
- Configuração para definir a pasta onde salvar as notícias como pdf.
  [Felipe Lube de Bragança]
- Impl. inicial do job para salvar a notícia como pdf. [Felipe Lube de
  Bragança]
- Possibilidade de status mais granulares e adição de status. [Felipe
  Lube de Bragança]
- Atualização e organização dos requisitos. [Felipe Lube de Bragança]
- Adicionada a dependência pdfkit para baixar as páginas. [Felipe Lube
  de Bragança]
- Renomeação da coluna de `Baixado` para `status` [Felipe Lube de
  Bragança]
- Atualização do pipfile com as dependências. [Felipe Lube de Bragança]
- Utilize o app django_rq. [Felipe Lube de Bragança]
- Implementação básica de app para buscar notícias. [Felipe Lube de
  Bragança]
- Atualização do changelog. [Felipe Lube de Bragança]
- Configuração básica para o logger. [Felipe Lube de Bragança]
- Adicione mais um status para situações de erro. [Felipe Lube de
  Bragança]
- Substitua um campo booleano downloaded por um com status múltiplos.
  [Felipe Lube de Bragança]
- Importação de requisitos em changelog do projeto no Drupal. [Felipe
  Lube de Bragança]
- Nova migração para o app user. [Felipe Lube de Bragança]
- App inicial para o tipo de conteúdo de notícia arquivada. [Felipe Lube
  de Bragança]
- Ignore arquivos do vscode. [Felipe Lube de Bragança]
- Template inicial baseada em jpadilla/django-project-template. [Felipe
  Lube de Bragança]
- Adicionado pylint. [Felipe Lube de Bragança]
- Adicionado o Django 2.1.4. [Felipe Lube de Bragança]
- Commit inicial. [Felipe Lube de Bragança]


