$(document).ready(function() {
  $('.flexslider').flexslider({
    animation: "slide"
  });
});

$(document).ready(function() {
	$('.imageBU').hover(function () {
		$('.textBU').fadeIn();
	}, function () {
		$('.textBU').fadeOut();	
	});
});

$(document).ready(function () {

      $(window).scroll(function () {
          if ($(this).scrollTop() > 100) {
              $('.imageBU').fadeIn();
          } else {
              $('.imageBU').fadeOut();
          }
      });

      $('.imageBU').click(function () {
          $("html, body").animate({
              scrollTop: 0
          }, 600);
          return false;
      });

  });