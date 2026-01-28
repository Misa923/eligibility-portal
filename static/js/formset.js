(function(){
  const addBtn = document.getElementById("add-row");
  const formsetDiv = document.getElementById("formset");
  const totalFormsInput = document.getElementById("id_clients-TOTAL_FORMS") || document.querySelector("input[name$='-TOTAL_FORMS']");
  const template = document.getElementById("empty-form-template");

  if(!addBtn || !formsetDiv || !totalFormsInput || !template) return;

  addBtn.addEventListener("click", () => {
    const total = parseInt(totalFormsInput.value, 10);

    const html = template.innerHTML
      .replace("__FIRST__", `<input type="text" name="clients-${total}-first_name" maxlength="80" id="id_clients-${total}-first_name" required>`)
      .replace("__MIDDLE__", `<input type="text" name="clients-${total}-middle_name" maxlength="80" id="id_clients-${total}-middle_name">`)
      .replace("__LAST__", `<input type="text" name="clients-${total}-last_name" maxlength="80" id="id_clients-${total}-last_name" required>`)
      .replace("__DOB__", `<input type="date" name="clients-${total}-dob" id="id_clients-${total}-dob" required>`)
      .replace("__DELETE__", `<input type="checkbox" name="clients-${total}-DELETE" id="id_clients-${total}-DELETE">`);

    const wrapper = document.createElement("div");
    wrapper.innerHTML = html.trim();
    formsetDiv.appendChild(wrapper.firstChild);

    totalFormsInput.value = String(total + 1);
    formsetDiv.lastElementChild.scrollIntoView({behavior:"smooth", block:"center"});
  });
})();
