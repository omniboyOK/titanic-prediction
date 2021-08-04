function handleSubmit(age, fare, parch, sibSp, Sex_male) {
  // show loader
  let loader = document.getElementById("loader");
  loader.classList.remove("d-none");

  fetch(
    `/predict?Age=${age}&Fare=${fare}&Parch=${parch}&SibSp=${sibSp}&Sex_male=${Sex_male}`
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
