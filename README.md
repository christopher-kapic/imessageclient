# imessageclient

**A work-in-progress with Ian Cramer**

This is a self-hosted webapp for people with a (spare) Mac to send and receive iMessage messages on non-iOS devices.


## 2021 Update and Plan
In 2021, when I (Christopher, potentially Ian) have more free time, I am going to revisit this project. When that happens, this is the plan:
 - Switch to NodeJS
 - There will actually be two servers. In order to prevent users from exposing a port on their home wifi, we will instead use a cloud computer to host the website. There will be two types of clients: home servers and users.
 - Implement websockets to send messages between the home server and the cloud server; implement websockets to send messages between the cloud server and the user. (This is how we can avoid exposing a port on someone's home wifi)
 - Implement a simple database for storing user and home server information (with secure practices like hashing passwords with `bcrypt`). (This could potentially allow multiple users to use the same cloud server)
