$(document).ready(function(){

    $('.navbar').css('background-color', 'rgba(0,123,255,.5)');
    $('.navbar').addClass('navbar-dark');
    var scroll_start = 0;
    var startchange = $('#startchange');
    var contentbox =  $('#content-box');
    var offset = startchange.offset();
    var offset2 = contentbox.offset();
    var scrollPosition = $("body, html").scrollTop()
    if (scrollPosition != 0){
        $('.navbar').css('background-color', '#007bff');
    }
    $(document).scroll(function() {
        scroll_start = $(this).scrollTop()
        if(scroll_start > offset.top) {
            $('.navbar').css('background-color', '#007bff');
        } else {
            $('.navbar').css('background-color', 'rgba(0,123,255,.5)');
        }
    });
});