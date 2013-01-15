/**
 * Functions for the translations
 *
 **/
var Sprak = {
    'root': '/sparky_client'
};

Sprak.init = function(){

};

/**
 *
 * @param [e]
 */
Sprak.hideForm = function(e){
    //$("#sprak-form").hide();
    //$("#sprak-sidebar a").removeClass("active");
};




$("#sprak-sidebar a").click(function(e){
    console.log('Hierzo');
    var pos = $(this).position();
    var width = $(this).outerWidth();
    var form = $("#sprak-form");

    form.show();
    form.css({
        'top': pos['top'],
        'left': pos['left'] + width
    });
    console.log("WW = " + JSON.stringify(pos));

    $("#sprak-sidebar a").removeClass("active");
    $(this).addClass("active");
    e.stopPropagation();
});

$("#sprak-sidebar").scroll(Sprak.hideForm);

$("#sprak-form").click(function(e){
    e.stopPropagation();
});

$(document).click(function(e){
    //console.log($(e.target).is(".sprak-form"));
    Sprak.hideForm();
    //$("#sprak-form").hide();
});



//Deprecated
$("span[contenteditable]").click(function(e){
    var text = $(this).html();
    var pos = $(this).position();
    var id = $(this).attr('id');

    console.log("Pos = " + JSON.stringify(pos) + ", " + id);
    $('#s-' + id).trigger('click');
    //$('#s-4a6a59aa75d28c79e8e9485d5019ddd9').trigger('click');
    console.log('Jawel');



    //console.log("Text: " + text + ", " + JSON.stringify(pos));

    /*
    $.getJSON("https://www.googleapis.com/language/translate/v2?key=AIzaSyDL6a0wb7JAf8Aj2ud51j4BcssPBVmaWr4&source=nl&target=en&q=" + text + "&callback=?",{},
function(data){
    console.log("json callback = " + JSON.stringify(data));
    $("#google").html(data['data']['translations'][0]['translatedText']);
    });
    */
});


$("a").click(function(e)
{
    var id = $(this).attr('id');

    console.log("DDD = " + id);
    //e.preventDefault();
});
