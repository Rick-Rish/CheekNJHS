
const container = document.getElementById("container");
const registerBtn = document.getElementById("register");
const loginBtn = document.getElementById("login");

registerBtn.addEventListener("click", () => {
  container.classList.add("active");
});

loginBtn.addEventListener("click", () => {
  container.classList.remove("active");
});

const logWelcome = document.getElementById("greetingsign");
const logHour = new Date().getHours();

let logGreeting;

 if (logHour < 12) {
    logGreeting = "Good Morning, Friend!";
 } else if (logHour < 18) {
    logGreeting = "Good Afternoon, Friend!";
 } else {
    logGreeting = "Good Evening, Friend!";
 }

logWelcome.innerText = logGreeting;
 console.log(logGreeting)
 console.log("Current hour:", new Date().getHours());
