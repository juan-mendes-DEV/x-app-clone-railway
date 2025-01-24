const button = document.getElementById('dropdownButton');
const menu = document.getElementById('dropdownMenu');
const buttonn = document.getElementById('dropdownButtoN');
const menuu = document.getElementById('dropdownMenU');

button.addEventListener('click', () => {
  menu.classList.toggle('show'); // Alterna a classe "show"
});

buttonn.addEventListener('click', () => {
  menuu.classList.toggle('show'); // Alterna a classe "show"
});

window.addEventListener('click', (event) => {
  if (!buttonn.contains(event.target)) {
    menuu.classList.remove('show');
  }
});
// Fecha o dropdown ao clicar fora
window.addEventListener('click', (event) => {
  if (!button.contains(event.target)) {
    menu.classList.remove('show');
  }
});