let global_data;
let global_vars;

function loadConversation(cont) {
    document.getElementById("active-con-header").innerHTML = cont;
    for (i = 0; i < global_data.length; i++) {
        if (global_data[i]["contact"] == cont) {
            for (const message of global_data[i]["messages"]) {
                if (message[0] == 0) { // other person
                    document.getElementById("message-box").innerHTML += '<p>' + message[1] + '</p>';
                } else { // user
                    document.getElementById("message-box").innerHTML += '<p>' + message[1] + '</p>';
                }
            }
        }
    }
    document.getElementById("pending-message-text").addEventListener('submit', sendText);
}

function firstLoadMessages() {
    fetch("/api/init")
        .then(res => {
            if (res.ok) {
                console.log('Success.');
            } else {
                console.log("Failed to retrieve messages.");
                alert("Failed to retrieve messages.");
            }
            return res.json();
        })
        .then(data => {
            console.log(data);
            global_data = data;
            for (i = 0; i < data.length; i++) {
                document.getElementById("conversations").innerHTML += '<div class="conversation"><h1 class="conversation-contact">' + data[i]["contact"] + '<h1><p class="conversation-latest">' + data[i]["messages"][0][1] + '<p><div>';
            }
            loadConversation(data[0]["contact"]);
        })
}

function sendText() {
    let mymes = document.getElementById("pending-message-text").value;
    fetch("/api/message", {
        method: 'POST',
        body: {
            "recipient": "Ian Cramer",
            "text": mymes
        }
    })

}

function showAlert() {
    alert("Hello World!");
}

