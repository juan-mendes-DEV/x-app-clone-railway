const button = document.getElementById('dropdownButton');
const menu = document.getElementById('dropdownMenu');
const buttonn = document.getElementById('dropdownButtoN');
const menuu = document.getElementById('dropdownMenU');

button.addEventListener('click', () => {
  event.stopPropagation();
  menu.classList.toggle('show'); // Alterna a classe "show"
  menuu.classList.remove('show');
});

buttonn.addEventListener('click', () => {
  event.stopPropagation();
  menuu.classList.toggle('show'); // Alterna a classe "show"
  menu.classList.remove('show');
});

menuu.addEventListener('click', (event) => {
  event.stopPropagation(); // Impede que o clique dentro do dropdown feche o menu
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