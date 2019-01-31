const plugEditors = function() {
  const elements = document.querySelectorAll("div.quill-widget-content");
  const plugEditor = function(el) {
    return new Quill(el, {
      modules: {
        toolbar: ["bold", "italic", "underline", "strike"]
      },
      placeholder: "",
      readOnly: false,
      theme: "snow"
    });
  };
  elements.forEach(element => {
    const quillEditor = plugEditor(element);
    const editorForm = element.closest("form");
    const textArea = element.parentElement.querySelector("textarea");
    quillEditor.textArea = textArea;

    const populateTextArea = function() {
      const textarea_value = this.quillEditor.root.innerHTML;
      this.textArea.innerHTML = textarea_value;
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
