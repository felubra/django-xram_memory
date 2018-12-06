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

# Publicação

- Logotipo
- Configurações de extração: se somente estilo de impressão, se usa javascript ou não etc.
