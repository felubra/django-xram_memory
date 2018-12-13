# Changelog

Todas as mudanças notáveis neste projeto estarão listadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Versionamento semântico](https://semver.org/spec/v2.0.0.html).

## [Não publicado]
- Segue abaixo funcionalidades para serem feitas ou ainda não publicadas.

### Adicionado

#### Tipos de conteúdo
- Notícia arquivada
- Documento
- Imagem
- Coleção: conjunto curado dos tipos de conteúdo acima

#### Auditoria
- Use a classe LogEntry do Django para manter um histórico de alterações
- Logue todas as ações realizadas para o STDOUT
- Faça um relatório da captura da notícia em PDF
- Faça um perfil de Auditor

#### Captura
- Capture a notícia em formato PDF
- Capture a notícia em formato HTML
- Capture a notícia em formato de Imagem

#### Integração com o Archive.org
- Busque a URL da notícia, se houver arquivo dela

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

### Obsoleto

### Removido

### Corrigido

### Segurança
