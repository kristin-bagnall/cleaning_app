"use strict";

// Homepage

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

  // Shrink the navbar 
  navbarShrink();

  // Shrink the navbar when page is scrolled
  document.addEventListener('scroll', navbarShrink);

  // Activate Bootstrap scrollspy on the main nav element
  const mainNav = document.body.querySelector('#mainNav');
  if (mainNav) {
      new bootstrap.ScrollSpy(document.body, {
          target: '#mainNav',
          offset: 74,
      });
  };

  // Collapse responsive navbar when toggler is visible
  const navbarToggler = document.body.querySelector('.navbar-toggler');
  const responsiveNavItems = [].slice.call(
      document.querySelectorAll('#navbarResponsive .nav-link')
  );
  responsiveNavItems.map(function (responsiveNavItem) {
      responsiveNavItem.addEventListener('click', () => {
          if (window.getComputedStyle(navbarToggler).display !== 'none') {
              navbarToggler.click();
          }
      });
  });

});



// Bend service area map
function initMap() {
  const map = new google.maps.Map(document.getElementById("service-area-map"), {
    zoom: 9,
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




// ---

  // Closes responsive menu when a scroll trigger link is clicked
$(".js-scroll-trigger").click(function () {
    $(".navbar-collapse").collapse("hide");
});

// Activate scrollspy to add active class to navbar items on scroll
$("body").scrollspy({
    target: "#mainNav",
    offset: 100,
});

// Collapse Navbar
var navbarCollapse = function () {
    if ($("#mainNav").offset().top > 100) {
        $("#mainNav").addClass("navbar-shrink");
    } else {
        $("#mainNav").removeClass("navbar-shrink");
    }
};
// Collapse now if page is not at top
navbarCollapse();
// Collapse the navbar when page is scrolled
$(window).scroll(navbarCollapse);


// customer portal log out functionality
const logOut = $('#log-out')

logOut.on('click', () =>{
  fetch(`/logout`)
})


$('#reviewModal').on('show.bs.modal', (event) => {
  console.log('hello');
  const modal = $('#reviewModal');
  const button = $(event.relatedTarget); // Button that triggered the modal
  const user_first_name = button.data('user_first_name');
  const job_id = button.data('job_id');

  
  modal.find('.modal-title').text(user_first_name + ', we appreciate your feedback');
  $('#modal_job_id').val(job_id);
});

