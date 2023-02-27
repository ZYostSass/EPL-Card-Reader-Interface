// Add color overlay on equipment images
$('ul.list-unstyled > li > a[href="' + document.location.pathname + '"]').parent().addClass('active');

// Collapsible sidebar
$('.open-btn').on('click', function () {
  $('.sidebar').addClass('active');
});
$('.close-btn').on('click', function () {
  $('.sidebar').removeClass('active');
});