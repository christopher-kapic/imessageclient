let global_data;
let global_vars;

function loadConversation(cont) {
    document.getElementById("active-con-header").innerHTML = cont;
    for (i = 0; i < global_data.length; i++) {
        if (global_data[i]["contact"] == cont) {
            for (const message of global_data[i]["messages"]) {
                if (message[0] == 0) { // other person
                    document.getElementById("message-box").innerHTML += '<div class="holder"><p class="from-other">' + message[1] + '</p></div>';
                } else { // user
                    document.getElementById("message-box").innerHTML += '<div class="holder><p class="from-user">' + message[1] + '</p></div/';
                }
            }
        }
    }

}

function startConversation() {
    contact_ = window.prompt("To:", "contact");
    message_ = window.prompt("Message:", "");
    fetch("/api/message", {
        method: 'POST',
        body: JSON.stringify({
            "recipient": contact_,
            "text": message_
        })
    })
    // firstLoadMessages();
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
    alert("ALERT0");
    // mes = document.getElementById("pending-message-text").target.value;
    // alert("ALERT1");
    // fetch("/api/message", {
    //     method: 'POST',
    //     body: {
    //         "recipient": "Ian Cramer",
    //         "text": "test"
    //     }
    // })

}

function showAlert() {
    mes = document.getElementById("pending-message-text").value;
    // alert(mes)
    fetch("/api/message", {
        method: 'POST',
        body: JSON.stringify({
            "recipient": "Christopher Kapic",
            "text": mes
        })
    })
    document.getElementById("pendint-message-text").value = "";
}

function getRecipient() {

}

// document.getElementById("pending-message-text").addEventListener('submit', sendText);

// var content_of_message = document.getElementById("pending-message-text");
// content_of_message.addEventListener("keyup", (e) => {
//     e.preventDefault();
//     if (e.keyCode === 13) {
//         alert("hi")
//         sendText(content_of_message.target.value);
//     }
// })