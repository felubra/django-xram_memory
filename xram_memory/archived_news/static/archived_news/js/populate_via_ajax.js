(function($) {
  const fetchBasicInfo = function() {
    const url = $("input#id_url").val();

    $.post(basic_info_endpoint, {
      csrfmiddlewaretoken: CSRF_TOKEN,
      url: url
    })
      .done(function(data) {
        /**
         * * TODO: Transformações necessárias nos dados recebidos
         *
         * - published_date: necessário separar em duas partes, data e hora, para preenchermos dois campos:
         *  'published_date_0' e 'published_date_1'
         * - keywords: necessário adicionar um atributo selected a cada option que corresponder o value
         * - top_image: necessário fazer o upload do arquivo para o django ou inserir a imagem como value codificado em
         *   base64
         * - images: não implementado ainda
         * - summary, text e title e keywords: sem necessidade de transformação
         *
         * * TODO: Fazer um dicionário relacionando os campos recebidos no documento JSON com os campos a serem
         *  preenchidos no formulário HTML.
         *
         * * TODO: Preencher os campos, se possível com alguma indicação (uma breve animação na borda) de que o campo
         *  foi preenchido.
         */
      })
      .fail(function(err) {
        /**
         * * TODO: exibir uma mensagem de erro, nem que seja um simples alert.
         */
      });
  };

  const createButton = function() {
    const button = document.createElement("button");
    button.innerText = "Obter informações automaticamente";

    $(button).on("click", function(e) {
      e.preventDefault();
      return fetchBasicInfo();
    });

    return button;
  };

  const insertButton = function(button) {
    /**
     * * TODO: inserir depois do título (<h2>) do fieldset
     */
    $("fieldset.auto_insert_options").prepend(button);
  };

  const init = function() {
    const button = createButton();
    insertButton(button);
  };

  init();
})(django.jQuery);
