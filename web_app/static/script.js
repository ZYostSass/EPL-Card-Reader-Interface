// Add color overlay on equipment images
$('ul.list-unstyled > li > a[href="' + document.location.pathname + '"]').parent().addClass('active');

// Collapsible sidebar
$('.open-btn').on('click', function () {
  $('.sidebar').addClass('active');
});
$('.close-btn').on('click', function () {
  $('.sidebar').removeClass('active');
});

// Login window popup
const center = document.querySelector('.center');
const loginPopup = document.querySelector('.btn.btn-primary.login-popup');

loginPopup.addEventListener('click', () => {
  if (center.classList.contains('active-popup')) {
    closePopup(center);
  }
  else {
    openPopup(center);
  }
});

function openPopup(popup) {
  popup.classList.add('active-popup');
}

function closePopup(popup) {
  popup.classList.remove('active-popup');
}
