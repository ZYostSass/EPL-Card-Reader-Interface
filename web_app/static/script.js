$(function () {
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
  if (loginPopup != null) {
    loginPopup.addEventListener('click', () => {
      if (center.classList.contains('active-popup')) {
        closePopup(center);
      }
      else {
        openPopup(center);
      }
    });
  }

  // Student checkin popup
  const studentCheckin = document.querySelector(".student-checkin-content");
  if (studentCheckin != null) {
    if (document.URL.includes('/student-checkin')) {
      if (studentCheckin.classList.contains('active-popup')) {
        closePopup(studentCheckin);
      }
      else {
        openPopup(studentCheckin);
      }
    }

    studentCheckin.addEventListener('click', function (event) {
      event.stopPropagation();
    });
  }


  // Student Checkin Close
  const iconClose = document.querySelector('.icon-close')
  if (iconClose != null) {
    iconClose.addEventListener('click', function (event) {
      closePopup(studentCheckin);
    });
  }

  if (center != null) {
    center.addEventListener('click', function (event) {
      event.stopPropagation();
    });
  }

  function openPopup(popup) {
    popup.classList.add('active-popup');
    setTimeout(function () {
      popup.classList.remove('hidden');
    }, 300);
  }

  function closePopup(popup) {
    popup.classList.remove('active-popup');
    setTimeout(function () {
      popup.classList.add('hidden');
    }, 300);
  }

  $("#scan-btn").on("click", function (event) {
    event.preventDefault();  // Prevent default link behavior
    fetch("/card_data/")  // Make the request to the card_data route
      .then(response => response.json())  // Parse the JSON response
      .then(data => {
        if (data.card_number) {
          window.location.href = "/permissions/" + data.card_number + "/";  // Redirect to the permissions route with card_number as a parameter
        }
      })
      .catch(error => {
        console.log(error);  // Handle any errors
      });
  });
});