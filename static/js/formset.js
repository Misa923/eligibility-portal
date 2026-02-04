(function(){
  const addBtn = document.getElementById("add-row");
  const formsetDiv = document.getElementById("formset");
  const totalFormsInput =
   //* document.getElementById("id_clients-TOTAL_FORMS") || *//
    document.querySelector('input[name="clients-TOTAL_FORMS"]');
    document.querySelector("input[name$='-TOTAL_FORMS']");
  const template = document.getElementById("empty-form-template");

  if(!addBtn || !formsetDiv || !totalFormsInput || !template) return;

  
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
    const total = parseInt(totalFormsInput.value, 10);

    const html = template.innerHTML
      .replaceAll("__FIRST__", `<input type="text" name="clients-${total}-first_name" maxlength="80" id="id_clients-${total}-first_name" required>`)
      .replaceAll("__MIDDLE__", `<input type="text" name="clients-${total}-middle_name" maxlength="80" id="id_clients-${total}-middle_name">`)
      .replaceAll("__LAST__", `<input type="text" name="clients-${total}-last_name" maxlength="80" id="id_clients-${total}-last_name" required>`)
      .replaceAll("__DOB__", `<input type="date" name="clients-${total}-dob" id="id_clients-${total}-dob" required>`)
      .replaceAll("__DELETE__", `<input type="checkbox" name="clients-${total}-DELETE" id="id_clients-${total}-DELETE">`);

    const wrapper = document.createElement("div");
    wrapper.innerHTML = html.trim();
    formsetDiv.appendChild(wrapper.firstChild);

    totalFormsInput.value = String(total + 1);
    formsetDiv.lastElementChild.scrollIntoView({behavior:"smooth", block:"center"});
  });
})();
