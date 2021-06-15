"use strict";

// Navbar

window.addEventListener('DOMContentLoaded', event => {

  // Navbar shrink function
  var navbarShrink = function () {
      const navbarCollapsible = document.body.querySelector('#mainNav');
      if (!navbarCollapsible) {
          return;
      }
      if (window.scrollY === 0) {
          navbarCollapsible.classList.remove('navbar-shrink')
      } else {
          navbarCollapsible.classList.add('navbar-shrink')
      }
  };

  // Shrink the navbar when page is scrolled
  document.addEventListener('scroll', navbarShrink);

});



// Bend service area map
function initMap() {
  const map = new google.maps.Map(document.getElementById("service-area-map"), {
    zoom: 8,
    center: { lat: 44.0582, lng: -121.3153 },
  });
  // Define the LatLng coordinates for the polygon's path.
  const serviceCords = [
    { lat: 44.4360, lng: -121.2307 },
    { lat: 44.4360, lng: -121.4898 },
    
    { lat: 44.1367, lng: -121.6876 },

    { lat: 43.8554, lng: -121.4898 },
    { lat: 43.8554, lng: -121.2307 },

    { lat: 44.1367, lng: -121.0579 },
  ];
  // Construct the polygon.
  const bendMap = new google.maps.Polygon({
    paths: serviceCords,
    strokeColor: "#DDA15E",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: "#DDA15E",
    fillOpacity: 0.3,
  });
  bendMap.setMap(map);
}



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

