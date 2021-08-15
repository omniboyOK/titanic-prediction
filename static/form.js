var classes = [];

function handleSubmit(age, parch, sibSp, sex_male, embarked, clase, cabin) {
  // show loader
  let loader = document.getElementById("loader");
  loader.classList.remove("d-none");

  fetch(
    `/predict?Age=${age}&Parch=${parch}&SibSp=${sibSp}&Sex_male=${sex_male}&Embarked=${embarked}&Class=${clase}&Cabin=${cabin}`
  )
    .then((response) => response.json())
    .then((data) => {
      // remove loader
      loader.classList.add("d-none");

      // show result card
      let card = document.getElementById("cardresult");
      // remove old styles
      card.classList.remove("bg-success");
      card.classList.remove("bg-danger");
      card.classList.remove("d-none");
      data.survived
        ? card.classList.add("bg-success")
        : card.classList.add("bg-danger");

      // set result text
      let result_text = document.getElementById("result");
      result_text.innerText = data.result;

      window.scrollTo(0, document.querySelector(".container").scrollHeight);
    })
    .catch((error) => {
      console.log(error);
    });
}

$(document).ready(function () {
  fetch(`/classes`)
    .then((response) => response.json())
    .then((data) => {
      // save clases
      classes = data;

      data.forEach((item) => {
        let option = new Option(item.descripcion, item.clase);
        /// jquerify the DOM object 'o' so we can use the html method
        $(option).html(item.descripcion);
        $("#clase").append(option);
      });
      // enable dropdown
      $("#clase").prop("disabled", false);
    })
    .catch((error) => {
      console.log("Failed to load classes", error);
    });

  $("#clase").on("change", () => loadCabins());
});

function loadCabins() {
  let value = $("#clase").val();
  let clase = classes.find((item) => item.clase == value);
  $("#cabin").html('<option value="" selected></option>');

  // if any class selected enable, if not disable
  clase
    ? $("#cabin").prop("disabled", false)
    : $("#cabin").prop("disabled", true);

  if (clase) {
    clase.cabinas.forEach((cabina) => {
      if (cabina.valor > 0) {
        let option = new Option(cabina.tipo, cabina.valor);
        /// jquerify the DOM object 'o' so we can use the html method
        $(option).html(cabina.tipo);
        $("#cabin").append(option);
      }
    });
  }
}
