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
- Coleção: conjunto curado dos tipos de conteúdo acima

#### Auditoria
- Faça um relatório da captura da notícia em PDF
- Faça um perfil de Auditor

#### Captura
- Capture a notícia em formato HTML
- Capture a notícia em formato de Imagem


#### Perfis de acesso:
- Visitante:
  - Pesquisa de notícias arquivadas
  - Vê o resumo da notícia arquivada e uma imagem ilustrativa
  - Tem acesso ao link original
- Membro:
  - Tem as permissões do Visitante
  - Tem acesso integral à notícia arquivada publicada, incluindo versão outros formatos
- Garimpador: poderá inserir novas notícias arquivadas
  - Pode editar uma notícia arquivada, mas não solicitar versão atualizada dela
- Moderador: poderá publicar notícias arquivadas
- Editor: poderá fazer as ações tanto do Garimpador como do Moderador
  - Pode solicitar nova versão de notícias arquivadas
- Auditor:
  - Acessa integralmente uma notícia arquivada, sem poder alterá-la
  - Tem acesso aos logs e relatórios relacionados à extração da notícia

#### Views
- Busca geral no site
  - Busca simples, estilo Google
  - Busca avançada
- Página de resultados, com filtros
- Lista de imagens/documentos/notícias com filtros
- Páginas básicas
  -  Inicial
  -  Sobre
  -  Contato
- Páginas individuais
  - Notícia arquivada
  - Documento
  - Imagem
  - Coleção

### Modificado
- O campo de palavras-chave no formulário de inserção/edição da Notícia Arquivada deve permitir a digitação direta das
  palavras-chave e deve ter uma interface melhor.
- O formulário de inserção da notícia arquivada deve ter manipuladores em javascript para restringir os campos quando o
  modo de inserção for alterado.

### Obsoleto

### Removido

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