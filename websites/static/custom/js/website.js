var div = $('.fixed-top');
    $(window).scroll(function(){
       if($(document).scrollTop()>12){
          var percent = $(document).scrollTop() / ($(document).height() - $(window).height());
          div.css('opacity', 0 + percent);
       }else{
          div.css('opacity', 0.2);
       }
    });

function returns_input_html(type, name, id, value, min, max, image, content){

    readonly = ""
    if (min == max) {
        readonly = "readonly"
    }

    if (type != "number") {
        return '<div class="form-check mr-2"> ' +
            '<input class="form-check-input" type='+type+' name='+name+' id='+id+' value='+value+' '+readonly+'> ' +
            '<label class="form-check-label btn-primary rounded p-1" for='+id+'> ' +
                image +
                content +
            '</label> ' +
        '</div>';
    }

    return '<div class="form-check mr-2"> ' +
        '<input class="form-control-input mr-1" type='+type+' name='+name+' id='+id+' '+
        'min='+min+' max='+max+' style="width:50px;" '+readonly+'>' +
        '<label class="form-control-input btn-primary rounded p-1" for='+name+'>' +
            image +
            content +
        '</label>' +
    '</div>';

}

function update_total_radio(previous_value, value){

    return value - previous_value;

}

function update_total_checkbox(checkbox, value){
    if (checkbox.is(":checked")) {
        return value;
    } else {
        return -value;
    }
}

function update_total_number(previous_value, number, value){

    if ($.isNumeric(number)) {
        return (parseInt(number) * value) - previous_value;
    } else {
        return 0
    }

}
