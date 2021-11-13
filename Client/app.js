var sendChat = document.querySelector("#button-addon2")

var userID = 12

/*
sendChat.onclick = function () {
  var you = document.querySelector("#you").value;
  var bot = document.querySelector("#bot")
  fetch("https://localhost:8080/chat?userID=test65&userInput=" + you)
    .then(response => response.json())
    .then(data => console.log(data))
  bot.value = data
  console.log(data)
}
*/

sendChat.onclick = function () {
  var userText = document.querySelector("#you").value;
  console.log("This is user input: ", userText);
  sendNewChat(userText);
}

function sendNewChat(userText) {
  var url = new URL("http://localhost:8080/chat");
  url.searchParams.set('userID', userID);
  url.searchParams.set('userInput', userText);
  console.log("This is url: ", url)

  fetch(url, {
    method: "GET",
    credentials: "include"
  }).then(function (response) {
    console.log("Server responded to GET chat request")


  })

}

// send chat
// changed so by parameters

function createNewUserMessage(message) {
  var data = "message=" + encodeURIComponent(message);
  fetch("localhost:8080/chat?userID=(userID)&userInput=(userInput)", {
    method: "POST",
    body: data,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    }
  }).then(function (response) {
    console.log("Message has been placed by the user!");
    loadUserMessage(message);
    loadBotMessage(message);
  });
}

function loadUserMessage(message) {
  var chatBoxHolder = document.querySelector(".chat");

  fetch("localhost:8080/chat?userID=(userID)&userInput=(userInput)&timeStamp=(timeStamp)" + String(message)).then(function (response) {
    response.json().then(function (data) {
      MESSAGE = data
      console.log("Message Loaded by the user:", MESSAGE);

      var chatBoxHolder = document.querySelector(".chat");

      data.forEach(function (message) {
        var newMessageDiv1 = document.createElement("div");
        newMessageDiv1.classList.add("media");
        newMessageDiv1.classList.add("w-50");
        newMessageDiv1.classList.add("ml-auto");
        newMessageDiv1.classList.add("mb-3");

        var newMessageDiv2 = document.createElement("div");
        newMessageDiv2.classList.add("media-body");

        var newMessageDiv3 = document.createElement("div");
        newMessageDiv3.classList.add("bg-primary");
        newMessageDiv3.classList.add("rounded");
        newMessageDiv3.classList.add("py-2");
        newMessageDiv3.classList.add("px-3");
        newMessageDiv3.classList.add("mb-2");

        var newMessageParagraph1 = document.createElement("p");
        newMessageParagraph1.classList.add("mb-0");
        newMessageParagraph1.classList.add("text-white");
        newMessageParagraph1.innerHTML = message;

        var newMessageParagraph2 = document.createElement("p");
        newMessageParagraph2.classList.add("small");
        newMessageParagraph2.classList.add("text-muted");
        newMessageParagraph2.classList.add("mb-0");
        // newMessageParagraph2.innerHTML = timestamp;
        // How do I get the timestamp?

        // Almost appending in reverse
        newMessageDiv3.appendChild(newMessageParagraph1);
        newMessageDiv2.appendChild(newMessageDiv3);
        newMessageDiv2.appendChild(newMessageParagraph2);
        newMessageDiv1.appendChild(newMessageDiv2);
      });
    });
  });
}

function loadBotMessage(message) {
  var chatBoxHolder = document.querySelector(".chat");

  fetch("localhost:8080/chat?userID=(userID)&userInput=(userInput)&timeStamp=(timeStamp)" + String(message)).then(function (response) {
    response.json().then(function (data) {
      MESSAGE = data
      console.log("Message Loaded by the bot:", MESSAGE);

      var chatBoxHolder = document.querySelector(".chat");

      data.forEach(function (message) {
        var newMessageDiv1 = document.createElement("div");
        newMessageDiv1.classList.add("media");
        newMessageDiv1.classList.add("w-50");
        newMessageDiv1.classList.add("mb-3");

        var newMessageDiv2 = document.createElement("div");
        newMessageDiv2.classList.add("media-body");
        newMessageDiv2.classList.add("ml-3");

        var newMessageDiv3 = document.createElement("div");
        newMessageDiv3.classList.add("bg-light");
        newMessageDiv3.classList.add("rounded");
        newMessageDiv3.classList.add("py-2");
        newMessageDiv3.classList.add("px-3");
        newMessageDiv3.classList.add("mb-2");

        var newMessageParagraph1 = document.createElement("p");
        newMessageParagraph1.classList.add("mb-0");
        newMessageParagraph1.classList.add("text-black");
        newMessageParagraph1.innerHTML = message;

        var newMessageParagraph2 = document.createElement("p");
        newMessageParagraph2.classList.add("small");
        newMessageParagraph2.classList.add("text-muted");
        newMessageParagraph2.classList.add("mb-0");
        // newMessageParagraph2.innerHTML = timestamp;
        // How do I get the timestamp?

        // Almost appending in reverse
        newMessageDiv3.appendChild(newMessageParagraph1);
        newMessageDiv2.appendChild(newMessageDiv3);
        newMessageDiv2.appendChild(newMessageParagraph2);
        newMessageDiv1.appendChild(newMessageDiv2);
      });
    });
  });
}
