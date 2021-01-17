var div = $('.fixed-top');
    $(window).scroll(function(){
       if($(document).scrollTop()>12){
          var percent = $(document).scrollTop() / ($(document).height() - $(window).height());
          div.css('opacity', 0 + percent);
       }else{
          div.css('opacity', 0.2);
       }
    });

function returns_html_input(type, name, id, min, max, image, content){

    readonly = ""

    if (type != "number") {

        if (min == max) readonly = "checked";

        return '<div class="form-check mr-2"> ' +
            '<input class="form-check-input" type='+type+' name='+name+' id='+id+' value='+id+
            ' '+readonly+'> ' +
            '<label class="form-check-label btn-primary rounded p-1" for='+id+'> ' +
                image +
                content +
            '</label> ' +
        '</div>';
    }

    if (min == max) readonly = "readonly";

    return '<div class="form-check mr-2"> ' +
        '<input class="form-control-input mr-1" type='+type+' name='+id+' id='+id+' '+
        'value='+min+' min='+min+' max='+max+' style="width:50px;" '+readonly+'>' +
        '<label class="form-control-input btn-primary rounded p-1" for='+id+'>' +
            image +
            content +
        '</label>' +
    '</div>';

}


function change_option_info(html, title, description, image) {

    $("#"+html+"_title").text(title);
    $("#"+html+"_description").text(description);

    $("#"+html+"_image").empty();

    if (image) {
        $("#"+html+"_image").html("<img src="+image+" class='img-fluid' " +
                "alt="+title+" style='max-height:400px;max-width:100%;'>");
    }
}
