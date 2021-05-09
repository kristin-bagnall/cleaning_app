"use strict";

const logOut = document.getElementById('log-out');

logOut.addEventListener('click', () =>{
  fetch(`/logout`)
})



// get_human_form.addEventListener('submit', (evt) => {
//   evt.preventDefault();

//   const human_id = document.querySelector('#human-id').value;

//   fetch(`/api/human/${human_id}`)
//   .then(response => response.json())
//   .then(data => {
//     document.querySelector('#fname').innerText = data.fname; 
//     document.querySelector('#lname').innerText = data.lname; 
//     document.querySelector('#email').innerText = data.email; 
//   });
// });