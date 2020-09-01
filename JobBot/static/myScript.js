function getBotResponse() {

  // Récupération du texte en brut depuis l'input
  var rawText = $("#textInput").val();

  // Transformation du texte brut en <p>
  var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";

  // Vide le text input
  $("#textInput").val("");

  // Ajoute Le <p> du user à la div
  $("#chatbox").append(userHtml);

  document
    .getElementById("userInput")
    .scrollIntoView({ block: "start", behavior: "smooth" });

  // Appel Ajax pour récupérer la réponse du bot
  $.get("/get", { msg: rawText }).done(function(data) {
    var botHtml = '<p class="botText"><span>' + data + "</span></p>";
    $("#chatbox").append(botHtml);

    document
      .getElementById("userInput")
      .scrollIntoView({ block: "start", behavior: "smooth" });
  });
}

function saveConv() {
  console.log("In saveConv")

  var conv = $('chatbox').find('p').text()

  console.log("Conv : ", conv)

}

$("#textInput").keypress(function(e) {
  if (e.which == 13) {
    getBotResponse();
    // saveConv();
  }
});
