(function () {
  const addBtn = document.getElementById("add-row");
  const formsetDiv = document.getElementById("formset");
  const totalFormsInput = document.querySelector('input[name="clients-TOTAL_FORMS"]');
  const template = document.getElementById("empty-form-template");

  if (!addBtn || !formsetDiv || !totalFormsInput || !template) return;

  // Hide a row when DELETE is checked (for existing rows in a can_delete formset)
  formsetDiv.addEventListener("change", (e) => {
    const cb = e.target;
    if (!(cb instanceof HTMLInputElement)) return;
    if (cb.type !== "checkbox") return;
    if (!cb.name.endsWith("-DELETE")) return;

    const row = cb.closest(".client-row");
    if (!row) return;

    row.style.display = cb.checked ? "none" : "";
  });

  addBtn.addEventListener("click", () => {
    const index = parseInt(totalFormsInput.value, 10);

    // empty_form uses __prefix__ placeholders; replace them with the next index
    const html = template.innerHTML.replaceAll("__prefix__", String(index));

    const wrapper = document.createElement("div");
    wrapper.innerHTML = html.trim();
    const newRow = wrapper.firstElementChild;

    if (!newRow) return;

    formsetDiv.appendChild(newRow);
    totalFormsInput.value = String(index + 1);

    newRow.scrollIntoView({ behavior: "smooth", block: "center" });
  });
})();
