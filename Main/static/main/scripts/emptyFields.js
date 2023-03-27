function emptyAllFields() {
  let fields = document.getElementsByClassName("form-control");
  let i = 0;
  for (i = 0; i < 10; i++) {
    fields[i].value = "";
  }
}
