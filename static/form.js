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

      // get result card
      let card = document.getElementById("cardresult");

      // reset result card state
      clearCard(card);

      // set result card styles
      data.survived ? setSuccessCard(card) : setFailureCard(card);

      // set result text
      let result_text = document.getElementById("result");
      result_text.innerText = data.result;

      // show result card
      card.classList.remove("d-none");

      // Chart
      let barColor = data.percentile >= 50 ? "#C2F784" : "#FF2626";

      let chartContainer = document.getElementById("chart-container");

      chartContainer.innerHTML = `<div class="h2" id="percentile"></div><canvas id="my-chart" width="250" height="250"></canvas>`;

      let ctx = document.getElementById("my-chart").getContext("2d");

      let doughnutChart = new Chart(ctx, {
        type: "doughnut",
        data: {
          datasets: [
            {
              label: "Probabilidad de supervivencia",
              data: [data.percentile, 100 - data.percentile],
              backgroundColor: [barColor, "rgb(255, 255, 255)"],
              hoverOffset: 4,
            },
          ],
          labels: ["", ""],
        },
        options: {
          tooltips: { enabled: false },
          hover: { mode: null },
          borderRadius: 10,
          cutout: "80%",
          events: [],
          plugins: {
            legend: {
              display: false,
            },
          },
        },
      });

      document.getElementById("percentile").innerText = data.percentile + "%";

      window.scrollTo(0, document.querySelector(".container").scrollHeight);
    })
    .catch((error) => {
      console.log(error);
    });
}

function submitModel(age, parch, sibSp, sex_male, embarked, clase, cabin) {
  // show loader
  let loader = document.getElementById("loader");
  loader.classList.remove("d-none");

  fetch(
    `/usemodel?Age=${age}&Parch=${parch}&SibSp=${sibSp}&Sex_male=${sex_male}&Embarked=${embarked}&Class=${clase}&Cabin=${cabin}`
  )
    .then((response) => response.json())
    .then((data) => {
      // remove loader
      loader.classList.add("d-none");

      // get result card
      let card = document.getElementById("cardresult");

      // reset result card state
      clearCard(card);

      // set result card styles
      data.survived ? setSuccessCard(card) : setFailureCard(card);

      // set result text
      let result_text = document.getElementById("result");
      result_text.innerText = data.result;

      // show result card
      card.classList.remove("d-none");

      window.scrollTo(0, document.querySelector(".container").scrollHeight);
    })
    .catch((error) => {
      console.log(error);
    });
}

$(document).ready(function () {
  // Tooltip initialization
  let tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

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
        let option = new Option("Cabina " + cabina.tipo, cabina.tipo);
        /// jquerify the DOM object 'o' so we can use the html method
        $(option).html("Cabina " + cabina.tipo);
        $("#cabin").append(option);
      }
    });
  }
}

function setSuccessCard(card) {
  card.classList.add("border-success");
  card.classList.add("text-success");
}

function setFailureCard(card) {
  card.classList.add("border-danger");
  card.classList.add("text-danger");
}

function clearCard(card) {
  // remove old styles
  card.classList.remove("border-success");
  card.classList.remove("border-danger");
  card.classList.remove("text-success");
  card.classList.remove("text-danger");
  card.classList.add("d-none");
}
