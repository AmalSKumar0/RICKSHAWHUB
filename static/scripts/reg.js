let login = document.querySelector('.login');
let reg = document.querySelector('.disable');
let regbtn = document.querySelector('.regbtn');
let logbtn = document.querySelector('.logbtn');

regbtn.addEventListener('click', () => {
  reg.setAttribute('class', 'register');
  login.setAttribute('class', 'disable');
});

logbtn.addEventListener('click', () => {
  reg.setAttribute('class', 'disable');
  login.setAttribute('class', 'login');
});

let cross = document.querySelector('.cross');
cross.innerHTML = "\u00d7";
