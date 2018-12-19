# Changelog

Todas as mudanças notáveis neste projeto estarão listadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Versionamento semântico](https://semver.org/spec/v2.0.0.html).

## [Não publicado]

- Segue abaixo funcionalidades para serem feitas ou ainda não publicadas.

### Adicionado

#### Tipos de conteúdo

- Documento
- Imagem
- Coleção: conjunto curado de notícias arquivadas e/ou documentos

#### Auditoria

- Faça um relatório da captura da notícia em PDF
- Faça um perfil de Auditor

#### Captura

- Capture a notícia em formato HTML
- Capture a notícia em formato de Imagem
- Todas as capturas são instâncias de documentos

#### Perfis de acesso:

- Adicionar os perfis visitante, membro, garimpador, moderador, editor e auditor (mais informações no arquivo de
  requisitos)

#### Views

#### Interface administrativa
##### Notícia Arquivada
###### Lista geral
- Ícones para indicar a presença de capturas, ao invés de descrição textual do status
- Link para a notícia no título

#### Views

#### Página de busca geral no site
- Faça uma busca multi-facetada
- Utilize o ElasticSearch
- Busca com interface simples, estilo Google
- Link para página de busca avançada, com critérios

#### Página de resultados
- Filtros para limitar os resultados de acordo com critérios

#### Páginas básicas
  - Inicial
  - Sobre
  - Contato
#### Páginas individuais
  - Notícia arquivada
  - Documento
  - Imagem
  - Coleção

### Modificado

#### Views
##### Interface administrativa
###### Notícia Arquivada
####### Página individual de edição/adição
- Não salvar as flags no modelo, usá-las apenas no controller (formulário)
- Atualizar texto descritivo na área `avançado`
- O campo de palavras-chave no formulário de inserção/edição da Notícia Arquivada deve permitir a digitação direta das
  palavras-chave e deve ter uma interface melhor.
- O formulário de inserção da notícia arquivada deve ter manipuladores em javascript para restringir os campos quando o
  modo de inserção for alterado.

#### Tipos de conteúdo
##### Notícia arquivada
- Permita várias capturas de página por notícia arquivada

#### Captura
- [OK] Transforme a captura de página de uma notícia arquivada numa instância do tipo de conteúdo documento.
- Permita várias capturas de página por notícia arquivada

### Obsoleto

### Removido
- Não persista flags de modelo, utilize apenas o controller para definir, quando for salvar o modelo qual o
  processamento deve ser feito ou não.

### Corrigido

### Segurança

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
