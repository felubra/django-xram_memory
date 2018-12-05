# Requisitos de Entidade

## Archived News (notícia arquivada)

- Campos
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
- Toda alteração criará uma revisão, sem possibilidade de se evitar isso
  - Isso inclui todas as vezes que o CRON rodar e pegar uma nova versão da notícia.
