# Premissa geral

Um acervo para guardar documentos, notícias e imagens sobre temas relacionados à memória da Esquerda.

# Requisitos Gerais

- Sistema de auditoria: sistema robusto para registrar ações de usuários, especialmente as relacionadas ao conteúdo do
  acervo = `Chain of evidence`
- Tipos de conteúdo:
  - Artefatos: os itens principais do acervo
    - Notícia
      - Uma notícia da web capturada em formato PDF
    - Arquivos do usuário (PDFs, imagens etc.)
  - Página
    - Uma página de conteúdo geral para o site ou um texto sobre determinado tema/assunto com referências a um ou mais
      artefato do acervo
  - Item de taxonomia
    - Assunto
    - Palavra-chave
- Grupos distintos de tipos de usuário:
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
- Integração com arquivos da Internet
  - Archive.org: verificação de uma versão arquivada para a notícia
- Taxonomia para classificação do conteúdo
  - Assuntos
  - Palavras-chave
- Views:
  - Páginas individuais de conteúdo
    - Página
    - Notícia
    - Arquivo
      - Imagem
      - Documento PDF
      - Documento genérico
    - Item de taxonomia
  - Página inicial
    - Estilo revista
    - Estilo mecanismo de busca
  - Página de resultados de busca
  - Página de contato
  - Páginas legais
    - Termos de uso
    - Privacidade
    - Licenças
- Indexação do conteúdo para facilitar busca `full text`

# Requisitos Específicos

## Sistema de auditoria

### Informações básicas que todo registro deve ter

- Tipo da ação (Criação, atualização e deleção)
- Nome do usuário que realizou a ação
- Identificação do objeto que sofreu a ação
- IP do usuário
- Data e hora da ação
- Estágio ou resultado da ação (iniciado, concluído, falha)

### Ações registradas pelo sistema por tipo de conteúdo

- TODOS
  - Criação
  - Atualização
  - Deleção
- Notícia
  - Captura de conteúdo
  - Captura de versão arquivada
  - Captura de página

#### Informações específicas por tipo de ação

##### Captura de página

- URL de captura
- Nome do arquivo gerado
- Tempo da operação

##### Captura de conteúdo

- Campos atualizados
- URL utilizada para obter os dados
- Biblioteca utilizada para obter os dados
- Tempo da operação
- Relatório de captura (arquivo pdf gerado pelo sistema)

##### Captura de versão arquivada

- Nome do arquivo
- Tempo da operação

## Tipos de conteúdo

### Artefato

#### Campos

##### Campos editáveis pelo usuário

- Título
- Teaser / Resumo / Descrição
- Taxonomia
  - Palavras-chave
  - Assuntos

##### Campos internos (preenchidos pelo sistema)

- Slug
- Datas padrão: criação e modificação
- Usuário de criação e modificação

### Notícia (`news`)

#### Campos (herda os campos do artefato)

##### Campos editáveis pelo usuário

- URL: o endereço da notícia
- URL no `archive.org`: o endereço da versão arquivada da notícia no Internet Archive
- Imagem: a imagem da notícia
- Corpo da notícia: o texto completo da notícia
- Data de publicação original
- Autor(es)

##### Campos internos (preenchidos pelo sistema)

- Hash (usado para cache)
- Data de captura

#### Captura automática

- O usuário pode automatizar a captura da notícia e seus campos de conteúdo apenas inserindo uma URL
- Uma versão em PDF da notícia poderá ser capturada

#### Revisões e histórico

- Toda alteração criará uma revisão, sem possibilidade de se evitar isso
- Uma nova revisão também será inserida quando o conteúdo for gerado automaticamente
- Um histórico de alterações deve estar disponível na administração

#### Validações

- Validador para o campo URL para testar basicamente se a URL existe e se temos acesso à ela.

### Arquivo do usuário (`user_file`)

#### Campos (herda os campos do artefato)

##### Campos editáveis pelo usuário

- Arquivo

##### Campos internos (preenchidos pelo sistema)

- Tipo (`mime_type`)
- Tamanho

#### Revisões e histórico

- Toda alteração criará uma revisão, sem possibilidade de se evitar isso

### Item de taxonomia (`taxonomy_item`)

#### Campos

##### Campos editáveis pelo usuário

- Nome

##### Campos internos (preenchidos pelo sistema)

- Slug

### Página

#### Campos

##### Campos editáveis pelo usuário

- Título
- Teaser / Resumo / Descrição
- Corpo do artigo
- Autor(es)
- Imagem
- Taxonomia
  - Palavras-chave
  - Assuntos
- Estágio de publicação
  - Rascunho
  - Publicado
  - Promovido à página inicial
  - Em destaque na página inicial
- Modo de exibição da imagem
  - Fundo
  - Destaque

##### Campos internos (preenchidos pelo sistema)

- Slug
- Datas padrão: criação e modificação
- Usuário de criação e modificação

## Views

### Páginas individuais de conteúdo

#### Página

- Imagem de fundo / destaque
- Título ou teaser
- Autores
- Data de publicação
- Corpo
- Artefatos referenciados no corpo
- Opções de compartilhamento

#### Notícia

- Título
- Exibição da notícia em PDF

- Tabela com detalhes:

  - Breve descrição (resumo)
  - Endereço original da notícia
  - Endereço original da notícia
  - URL no `archive.org`
  - Data de publicação original
  - Autor(es)
  - Data de captura

- Opções de compartilhamento

#### Página inicial

##### Estilo página de busca

- Entrada de busca
- Filtros

- Pesquisas recentes
- Pesquisas populares

##### Estilo revista

- Bloco com página em destaque
- Lista com cinco artigos em destaque
- Botão `carregar mais` ou lista infinita

#### Item de taxonomia

- Título com o nome
- Lista de artefatos ou páginas relacionados

#### Arquivo

##### Imagem

- Imagem
- Descrição
- Nome do arquivo
- Tamanho
- Dimensões

##### Documento PDF

- Visualização
- Descrição
- Nome do arquivo
- Tamanho

- Botão para download

##### Documento genérico

- Ícone
- Descrição
- Nome do arquivo
- Tamanho

- Botão para download

##### Página de resultados de busca

- Lista de todos os itens de conteúdo encontrados, classificados por tipo de conteúdo

#### Página de contato

- Formulário para enviar uma mensagem de contato
  - Nome
  - Assunto
  - Mensagem
  - CAPTCHA

#### Páginas legais
