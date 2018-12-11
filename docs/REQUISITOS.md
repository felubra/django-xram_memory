# Requisitos de Entidade

## Archived News (notícia arquivada)

### Campos

- URL
- Título (derivado)
- Imagens
  - Imagem thumbnail (a mesma usada pelos agregadores de rede social)
  - Imagem de captura
- Teaser
- Resumo
- Corpo da notícia
- Timestamps
  - Publicada
  - Acessada
  - Gravada
- Link
- Hash (usado para cache)
- Taxonomia
  - Palavras-chave
  - Categoria
  - Meio de comunicação
  - Idioma
- Usuários / Pessoas
  - Garimpeiro
  - Moderador
  - Jornalista original
- Informações de copyright

### Notas

- Toda alteração criará uma revisão, sem possibilidade de se evitar isso - isso inclui todas as vezes que o CRON rodar e pegar uma nova versão da notícia.
- Alguns veículos exigem que o usuário seja assinante para ter acesso à notícia. O sistema deverá logar com um usuário configurado para ter acesso às notícias, para então requisitar salvar a página da notícia corretamente.
- Fazer um validador para o campo URL para testar basicamente se a URL existe e se temos acesso à ela.
- Tentar recuperar a notícia do Archive.ORG ao invés de ir até o site.

## Publicação

- Logotipo
- Configurações de extração: se somente estilo de impressão, se usa javascript ou não etc.

# Requisitos de acesso

## Tipos de usuário

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
