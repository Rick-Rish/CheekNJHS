function showPage(pageId) {
  var pages = document.getElementsByClassName('page');
  for (var i = 0; i < pages.length; i++) {
    pages[i].style.display = 'none';
  }
  document.getElementById(pageId).style.display = 'block';
}
function closePage(pageId) {
  var pages = document.getElementsByClassName('page');
  for (var i = 0; i < pages.length; i++) {
    pages[i].style.display = 'block';
  }
  document.getElementById(pageId).style.display = 'none';
}

const slotFill = document.getElementById("in-slot")
let count = 0

slotFill.innerHTML = 0

function incrementslot(){
 count = count + 1
 slotFill.innerText = count
}

console.log(count)

const volWelcome = document.getElementById("volwelcome");
const volHour = new Date().getHours();

let volGreeting;

 if (volHour < 12) {
    volGreeting = "Good Morning, Rishon!";
 } else if (volHour < 18) {
    volGreeting = "Good Afternoon, Rishon!";
 } else {
    volGreeting = "Good Evening, Rishon!";
 }

 volWelcome.innerText = volGreeting;
 console.log(volGreeting)
 console.log("Current hour:", new Date().getHours());

