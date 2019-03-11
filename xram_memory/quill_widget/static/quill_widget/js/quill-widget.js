const plugEditors = function() {
  const elements = document.querySelectorAll("div.quill-widget");

  const plugEditor = function(el) {
    let toolbar = el.getAttribute("data-toolbar");
    if (toolbar) {
      toolbar = JSON.parse(toolbar);
    }
    const options = {
      placeholder:
        el.getAttribute("data-placeholder") ||
        el.getAttribute("placeholder") ||
        "",
      modules: {
        toolbar: toolbar
      },
      theme: el.getAttribute("data-theme") || "snow",
      formats: el.getAttribute("data-formats").split(","),
      readOnly: el.getAttribute("data-read-only") || false
    };
    const editorElement = el.querySelector("div.quill-widget-content");
    return new Quill(editorElement, options);
  };
  const handleMaximize = function(event) {
    if (screenfull.enabled) {
      const icon = this.button.querySelector("img");
      screenfull.on("change", () => {
        if (screenfull.isFullscreen) {
          icon.setAttribute(
            "src",
            "/static/material-design-icons/navigation/svg/production/ic_fullscreen_exit_18px.svg"
          );
        } else {
          icon.setAttribute(
            "src",
            "/static/material-design-icons/navigation/svg/production/ic_fullscreen_18px.svg"
          );
        }
      });
      screenfull.toggle(this.quillContainer);
    } else {
      alert(
        "Infelizmente o seu navegador não suporta exibição em tela inteira."
      );
    }
  };

  const addMaximizeButton = function(container) {
    const quillContainer = this.element;

    const span = document.createElement("span");
    span.classList.add("ql-formats");

    const button = document.createElement("button");
    button.setAttribute("type", "button");
    button.setAttribute("data-maximized", false);
    button.classList.add("ql-maximize");

    button.addEventListener(
      "click",
      handleMaximize.bind({ button, quillContainer })
    );

    icon = document.createElement("img");
    icon.setAttribute(
      "src",
      "/static/material-design-icons/navigation/svg/production/ic_fullscreen_18px.svg"
    );

    button.appendChild(icon);
    span.appendChild(button);
    container.appendChild(span);
  };
  elements.forEach(element => {
    const quillEditor = plugEditor(element);
    const toolbar = element.querySelector(".ql-toolbar");
    const editorForm = element.closest("form");
    const textArea = element.querySelector("textarea");

    const populateTextArea = function() {
      this.textArea.innerHTML = this.quillEditor.root.innerHTML;
    };

    editorForm.addEventListener(
      "submit",
      populateTextArea.bind({ quillEditor, textArea })
    );
    addMaximizeButton.apply({ element }, [toolbar]);
  });
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", plugEditors);
} else {
  plugEditors();
}
