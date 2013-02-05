/**
 * Functions for the translations
 *
 **/
var Sparky = {
    'root': '/sparky_client'
};

Sparky.init = function(){

};

/**
 *
 * @param [e]
 */
Sparky.hideForm = function(e){
    //$("#sprak-form").hide();
    //$("#sprak-sidebar a").removeClass("active");
};

/**
 * This is a nifty trick to place the cursor at the end of the text when the onfocus event is triggered
 * onfocus="var val=this.value; this.value=''; this.value= val;"
 * http://stackoverflow.com/questions/511088/use-javascript-to-place-cursor-at-end-of-text-in-text-input-element
 *
 * @param obj
 */
Sparky.moveCursorToEnd = function(obj){
    var value = obj.val(); //store the value of the element
    $(obj).focus().val(value);
};










$("#sprak-sidebar a").click(function(e){
    console.log('Hierzo');
    var pos = $(this).position();
    var width = $(this).outerWidth();
    var form = $("#sprak-form");
    var textarea = form.find('textarea');
    var span = $(this).parent().find('span');

    form.show();
    form.css({
        'top': pos['top'],
        'left': pos['left'] + width
    });

    textarea.focus();
    textarea.val(span.html());
    Sparky.moveCursorToEnd(textarea);


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


$(document).ready(function(){
    $.post('/sparky_client/ajax/message', {
        'source': 'Login',
        'lang': 'nl',
        'msg': 'inloggen'
    }).done(function(data){
            //alert(JSON.stringify(data));
    });
});