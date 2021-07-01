# imessageclient

**A work-in-progress with Ian Cramer**

This is a self-hosted webapp for people with a (spare) Mac to send and receive iMessage messages on non-iOS devices.


## 2021 Update and Plan
In 2021, when I (Christopher, potentially Ian) have more free time, I am going to revisit this project. When that happens, this is the plan:
 - Switch to NodeJS
    - Use [osa-imessage](https://github.com/wtfaremyinitials/osa-imessage) for sending and receiving messages on local macOS computer.
    - Host static files on Netlify, use cookies to store user data?
 - [RethinkDB](https://github.com/rethinkdb/rethinkdb) for storing messages.
