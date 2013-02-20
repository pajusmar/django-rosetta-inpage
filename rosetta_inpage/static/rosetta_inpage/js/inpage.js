/**
 * Functions for the translations
 *
 **/
var RosettaInpage = {
    'root': '/rosetta_inpage'
};

/**
 *
 */
RosettaInpage.init = function(){

};

/**
 *
 * @param [e]
 */
RosettaInpage.hideForm = function(e){
    //$("#rosetta-inpage-form").hide();
    //$("#rosetta-inpage-sidebar a").removeClass("active");
};

/**
 * This is a nifty trick to place the cursor at the end of the text when the onfocus event is triggered
 * onfocus="var val=this.value; this.value=''; this.value= val;"
 * http://stackoverflow.com/questions/511088/use-javascript-to-place-cursor-at-end-of-text-in-text-input-element
 *
 * @param obj
 */
RosettaInpage.moveCursorToEnd = function(obj){
    var value = obj.val(); //store the value of the element
    $(obj).focus().val(value);
};

/**
 *
 * @returns {boolean}
 */
RosettaInpage.submit = function(){
    return false;
};

















$("#rosetta-inpage-sidebar a").click(function(e){
    var pos = $(this).position();
    var width = $(this).outerWidth();
    var form = $("#rosetta-inpage-form");

    var input = form.find('input[name="source"]');
    var textarea = form.find('textarea');

    var source = $(this).parent().find('code[type="source"]');
    var msg = $(this).parent().find('code[type="msg"]').html();
    var translated = msg.substring(4, msg.length-3);

    var next = $(this).parent().next();
    form.find('input[name="next"]').val(next.children(':first').attr('id'));

    form.show();
    form.css({
        'top': pos['top'],
        'left': pos['left'] + width
    });

    input.val(source.html());
    textarea.focus();
    textarea.val(translated);
    RosettaInpage.moveCursorToEnd(textarea);


    $("#rosetta-inpage-sidebar a").removeClass("active");
    $(this).addClass("active");
    e.stopPropagation();

    /*
     source = request.POST.get('source', '')
     target_locale = request.POST.get('lang', '')
     target_msg = request.POST.get('msg', '')
     print "Banaan = ", str(source), ", ", str(target_locale), ", ", str(target_msg)
     */
});

$("#rosetta-inpage-sidebar").scroll(RosettaInpage.hideForm);

$("#rosetta-inpage-form").click(function(e){
    e.stopPropagation();
});

$(document).click(function(e){
    //console.log($(e.target).is(".rosetta-inpage-form"));
    RosettaInpage.hideForm();
    //$("#rosetta-inpage-form").hide();
});



//Deprecated
$("span[contenteditable]").click(function(e){
    var text = $(this).html();
    var pos = $(this).position();
    var id = $(this).attr('id');

    console.log("Pos = " + JSON.stringify(pos) + ", " + id);
    $('#s-' + id).trigger('click');
    //$('#s-4a6a59aa75d28c79e8e9485d5019ddd9').trigger('click');
});


$("a").click(function(e)
{
    var id = $(this).attr('id');

    //console.log("DDD = " + id);
    //e.preventDefault();
});


$(document).ready(function(){
    /*
    $.post('/rosetta_inpage/ajax/message', {
        'source': 'Login',
        'lang': 'nl',
        'msg': 'inloggen'
    }).done(function(data){
        //alert(JSON.stringify(data));
    });
    */


    var form = $("#rosetta-inpage-form");
    //form.find('textarea').attr('disabled', 'disabled');

    form.find("form").ajaxForm({
        beforeSubmit: function(data, jqForm, options){
            console.log("1=" + data);
            console.log("2=" + jqForm);
            console.log("3=" + options);
            $(jqForm).find('textarea').attr('disabled', 'disabled');
            $(jqForm).find('input[type=submit]').attr('value', 'Saving ...');
        },
        success: function(responseText, statusText, xhr, jqForm){
            console.log(JSON.stringify(responseText) + ", " + statusText);
            $(jqForm).find('textarea').removeAttr('disabled');
            $(jqForm).find('input[type="submit"]').attr('value', 'Save');

            var nextId = $(jqForm).find('input[name="next"]').val();
            $('#' + nextId).trigger('click');
        }
    });

});