(function($) {
  const fetchBasicInfo = function() {
    const url = $("input#id_url").val();

    $.post(basic_info_endpoint, {
      csrfmiddlewaretoken: CSRF_TOKEN,
      url: url
    })
      .done(function(data) {
        console.log(data);
      })
      .fail(function(err) {
        console.log(err);
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
    $("fieldset.auto_insert_options").prepend(button);
  };

  const init = function() {
    const button = createButton();
    insertButton(button);
  };

  init();
})(django.jQuery);
