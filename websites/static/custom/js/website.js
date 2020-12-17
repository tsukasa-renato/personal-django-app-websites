var div = $('.fixed-top');
    $(window).scroll(function(){
       if($(document).scrollTop()>12){
          var percent = $(document).scrollTop() / ($(document).height() - $(window).height());
          div.css('opacity', 0 + percent);
       }else{
          div.css('opacity', 0.2);
       }
    });