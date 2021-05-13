"use strict";

// customer portal log out functionality
const logOut = $('#log-out')

logOut.on('click', () =>{
  fetch(`/logout`)
})


$('#reviewModal').on('show.bs.modal', (event) => {
  const modal = $('#reviewModal');
  const button = $(event.relatedTarget); // Button that triggered the modal
  const user_first_name = button.data('user_first_name');
  const job_id = button.data('job_id');
  
  modal.find('.modal-title').text(user_first_name + ', we appreciate your feedback');
  $('#modal_job_id').val(job_id);
});