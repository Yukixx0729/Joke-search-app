const settings = document.getElementById("mySetting");
const btn = document.getElementById("dropbtn");
function dropdown() {
  settings.classList.toggle("show");
}

btn.addEventListener("click", dropdown);

window.onclick = function (event) {
  if (event.target != btn) {
    settings.classList.remove("show");
  }
};
