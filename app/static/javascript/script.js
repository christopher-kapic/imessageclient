

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
            for (i = 0; i < data.length; i++) {
                document.getElementById("conversations").innerHTML += '<div class="conversation"><h1 class="conversation-contact">' + data[i]["contact"] + '<h1><p class="conversation-latest">' + data[i]["messages"][0][1] + '<p><div>'
            }
        })
}

function showAlert() {
    alert("Hello World!");
}

