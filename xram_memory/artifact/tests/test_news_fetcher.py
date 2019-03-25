from xram_memory.artifact.news_fetcher import NewsFetcher


def test_fetch_web_title():
    title = NewsFetcher.fetch_web_title(
        "https://web.archive.org/web/20180402192047/https://www.gazetadopovo.com.br/educacao/pesquisa-do-mit-universidade-publica-gratuita-pode-prejudicar-alunos-de-baixa-renda-4dvkdiewbpxj24hl6lber8vhe/")
    assert title == "Pesquisa do MIT: universidade pública gratuita prejudica mais pobres | Gazeta do Povo"
