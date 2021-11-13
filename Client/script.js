var signInButton = document.querySelector("#btn-sign-in");
var registerButton = document.querySelector("#btn-register");



signInButton.onclick=function() {

  var email = document.querySelector("#floatingInput").value;
  var password = document.querySelector("#floatingPassword").value;
  var body = "userName=" + encodeURIComponent(email);
  body += "&userPassword=" + encodeURIComponent(password);

  fetch("http://localhost:8080/sessions", {
    method: "POST",
    credentials: "include",
    body: body,
    headers: {
      "Content-Type":"application/x-www-form-urlencoded"
    }
  }).then(function(response) {
    console.log("Server responded to POST request")

    if(response.status == 200) {
      alert('Sucessfully signed in: ' + email);
    } else if (response.status == 401) {
      alert('Failed to sign in')
    } else {
      alert("Try again " + String(response.status))
    }
  });

}

registerButton.onclick = function() {
  var email = document.querySelector("#floatingInput").value;
  var password = document.querySelector("#floatingPassword").value;
  var data = "userName=" + encodeURIComponent(email);
  data += "&userPassword=" + encodeURIComponent(password);

  fetch("http://localhost:8080/users", {
    method: "POST",
    credentials: "include",
    body: data,
    headers: {
      "Content-Type":"application/x-www-form-urlencoded"
    }
  }).then(function(response) {
    console.log("Server responded to POST request")

    if(response.status == 201) {
      alert('Sucessful Registration');
    } else if (response.status == 401) {
      alert('Email Taken')
    } else {
      alert("Try again " + String(response.status))
    }
  });
}
