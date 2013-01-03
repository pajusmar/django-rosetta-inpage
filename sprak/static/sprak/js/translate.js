/**
 * Functions for the translations
 *
 **/
var Sprak = {};

Sprak.init = function(){

};

/**
 *
 * @param [e]
 */
Sprak.hideForm = function(e){
    $("#sprak-form").hide();
    $("#sprak-sidebar a").removeClass("active");
};




$("#sprak-sidebar a").click(function(e){
    var pos = $(this).position();
    var width = $(this).outerWidth();
    var form = $("#sprak-form");

    form.show();
    form.css({
        'top': pos['top'],
        'left': pos['left'] + width
    });

    $("#sprak-sidebar a").removeClass("active");
    $(this).addClass("active");
    e.stopPropagation();
});

$("#sprak-sidebar").scroll(Sprak.hideForm);

$("#sprak-form").click(function(e){
    e.stopPropagation();
});

$(document).click(function(e){
    console.log($(e.target).is(".sprak-form"));
    Sprak.hideForm();
    $("#sprak-form").hide();
});



//Deprecated
$("span[contenteditable]").click(function(e){
    var text = $(this).html();
    var pos = $(this).position();

    console.log("Text: " + text + ", " + JSON.stringify(pos));

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
    //e.preventDefault();
});
