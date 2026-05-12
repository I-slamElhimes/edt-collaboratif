console.log("Chatbot JS chargé et prêt !");

// 1. Récupérer le jeton de sécurité
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// 2. La fonction d'envoi de message
async function sendMessage() {
  const input = document.getElementById("aiInput");
  const body = document.getElementById("aiChatBody");
  const message = input.value.trim();

  if (!message) return;

  console.log("Message envoyé :", message);

  // Afficher le message de l'utilisateur
  const userDiv = document.createElement("div");
  userDiv.className = "ai-message ai-message-user";
  userDiv.textContent = message;
  body.appendChild(userDiv);

  input.value = "";
  body.scrollTop = body.scrollHeight;

  // Afficher un petit indicateur de chargement
  const loadingDiv = document.createElement("div");
  loadingDiv.className = "ai-message ai-message-bot";
  loadingDiv.id = "ai-loading";
  loadingDiv.textContent = "...";
  body.appendChild(loadingDiv);
  body.scrollTop = body.scrollHeight;

  try {
    const response = await fetch("/chatbot/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `message=${encodeURIComponent(message)}`,
    });

    const data = await response.json();

    // Retirer le chargement et afficher la réponse
    const loader = document.getElementById("ai-loading");
    if (loader) loader.remove();

    const botDiv = document.createElement("div");
    botDiv.className = "ai-message ai-message-bot";
    botDiv.textContent = data.reply;
    body.appendChild(botDiv);
    body.scrollTop = body.scrollHeight;
  } catch (error) {
    console.error("Erreur Fetch:", error);
    const loader = document.getElementById("ai-loading");
    if (loader) loader.textContent = "Erreur : le serveur ne répond pas.";
  }
}

// 3. Gestionnaire de CLIC (Méthode robuste)
document.addEventListener("click", function (event) {
  // Si on clique sur le bouton OU sur l'icône à l'intérieur du bouton
  if (event.target.id === "aiSendBtn" || event.target.closest("#aiSendBtn")) {
    event.preventDefault(); // Empêche tout comportement par défaut
    sendMessage();
  }
});

// 4. Gestionnaire de Touche Entrée
document.addEventListener("keypress", function (event) {
  if (event.key === "Enter" && event.target.id === "aiInput") {
    event.preventDefault();
    sendMessage();
  }
});
