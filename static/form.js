function handleSubmit(age, fare, parch, sibSp) {
  fetch(`/predict?Age=${age}&Fare=${fare}&Parch=${parch}&SibSp=${sibSp}`)
    .then((response) => response.json())
    .then((data) => {
      let result_text = document.getElementById("result");
      result_text.innerText = data.result;
    })
    .catch((error) => {
      console.log(error);
    });
}
