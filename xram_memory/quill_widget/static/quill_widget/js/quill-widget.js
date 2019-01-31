const plugEditors = function() {
  const elements = document.querySelectorAll("div.quill-widget");

  const plugEditor = function(el) {
    let toolbar = el.getAttribute("data-toolbar");
    const options = {
      placeholder:
        el.getAttribute("data-placeholder") ||
        el.getAttribute("placeholder") ||
        "",
      modules: {
        toolbar: el.getAttribute("data-toolbar")
          ? el.getAttribute("data-toolbar").split(",")
          : null
      },
      theme: el.getAttribute("data-theme") || "snow",
      readOnly: el.getAttribute("data-read-only") || false
    };
    const editorElement = el.querySelector("div.quill-widget-content");
    return new Quill(editorElement, options);
  };
  elements.forEach(element => {
    const quillEditor = plugEditor(element);
    const editorForm = element.closest("form");
    const textArea = element.querySelector("textarea");

    const populateTextArea = function() {
      this.textArea.innerHTML = this.quillEditor.root.innerHTML;
    };

    editorForm.addEventListener(
      "submit",
      populateTextArea.bind({ quillEditor, textArea })
    );
  });
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", plugEditors);
} else {
  plugEditors();
}
