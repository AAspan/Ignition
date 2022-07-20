var firebaseConfig = {
    // your config code
apiKey: "AIzaSyAdd9FxfkdRtucyyGCY0ShlyklvzyqrdRs",
authDomain: "ignition-1bf3e.firebaseapp.com",
databaseURL: "https://ignition-1bf3e-default-rtdb.firebaseio.com/",
projectId: "ignition-1bf3e",
storageBucket: "ignition-1bf3e.appspot.com",
messagingSenderId: "74076369865",
appId: "1:74076369865:web:ffd34b99a10b0a08236e18",
 };
  // Initialize Firebase
firebase.initializeApp(firebaseConfig);
  
  // initialize database
const db = firebase.database();
  
  // get user's data
const username = prompt("Please tell Ignition your Name:");
  
  // submit form
  // listen for submit event on the form and call the postChat function
document.getElementById("message-form").addEventListener("submit", sendMessage);
  
  // send message to db
function sendMessage(e) {
e.preventDefault();
  
    // get values to be submitted
const timestamp = Date.now();
const messageInput = document.getElementById("message-input");
const message = messageInput.value;
  
    // clear the input box
messageInput.value = "";
  
    //auto scroll to bottom
document
      .getElementById("messages")
      .scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
  
    // create db collection and send in the data
db.ref("messages/" + timestamp).set({
      username,
      message,
});
}
  
  // display the messages
  // reference the collection created earlier
const fetchChat = db.ref("messages/");
  
  // check for new messages using the onChildAdded event listener
fetchChat.on("child_added", function (snapshot) {
    const messages = snapshot.val();
    const message = `<li class=${
      username === messages.username ? "sent" : "receive"
    }><span>${messages.username}: </span>${messages.message}</li>`;
    // append the message on the page
    document.getElementById("messages").innerHTML += message;
});