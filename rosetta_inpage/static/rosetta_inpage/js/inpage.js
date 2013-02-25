/***
 * Le JavaScript for Rosetta Inpage app.
 * Depends on jQuery.
 * https://github.com/citylive/django-rosetta-inpage
 *
 * Everything is wrapped in a closure to encapsulate all functionality. Public functionality is exposed in the end
 * of this file by assigning the Inpage object to the window object and expose it as RosettaInpage.
 *
 *
 * Ensure that jQuery and jQuery.form is loaded. If they're not loaded yet will do a document.write,
 * this is a blocking statement and will assure that both libraries are loaded before we include this javascript file.
 *
 * <script>!window.jQuery && document.write('<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js"><' + '/script>');</script>
 * <script>!window.jQuery().ajaxForm && document.write('<script src="//cdnjs.cloudflare.com/ajax/libs/jquery.form/3.24/jquery.form.js"><' + '/script>');</script>
 */
(function(window, document){
    'use strict';

    // Define some constants
    var ROOT = '/rosetta_inpage',
        PREFIX = 'rosetta-inpage',
        ID_SIDEBAR = PREFIX + '-sidebar',
        ID_FORM = PREFIX + '-form'
    ;


    /**
     * Define the namespace. All functions in this namespace are public.
     */
    var Inpage = {};


    /**
     * Initialize all links in the sidebar.  When the user clicks on it the form to translate will appear
     */
    function initLinks(){
        $('#' + ID_SIDEBAR + ' .' + PREFIX + '-content  a').click(function(e){
            var pos = $(this).position();
            var width = $(this).outerWidth();
            var form = $('#' + ID_FORM);

            var input = form.find('input[name="source"]');
            var textarea = form.find('textarea');

            var source = $(this).parent().find('code[type="source"]').html();
            var msg = $(this).parent().find('code[type="msg"]').html();

            var source_stripped = source.substring(4, source.length-3);
            var msg_stripped = msg.substring(4, msg.length-3);

            var next = $(this).parent().next();
            form.find('input[name="next"]').val(next.children(':first').attr('id'));

            form.show();
            form.css({
                'top': pos['top'],
                'left': pos['left'] + width
            });

            input.val(source_stripped);
            textarea.focus();
            textarea.val(msg_stripped);
            moveCursorToEnd(textarea);


            $('#' + ID_SIDEBAR + ' a').removeClass("active");
            $(this).addClass("active");
            e.stopPropagation();

            /*
             source = request.POST.get('source', '')
             target_locale = request.POST.get('lang', '')
             target_msg = request.POST.get('msg', '')
             print "Banaan = ", str(source), ", ", str(target_locale), ", ", str(target_msg)
             */
        });
    }


    /**
     * Attach ajax functionality to the translation form.
     * Depends on http://cdnjs.cloudflare.com/ajax/libs/jquery.form/3.24/jquery.form.js
     */
    function initForm(){
        var $form = $('#' + ID_FORM);
        var $alert = $form.find('.rosetta-inpage-alert');

        $form.find('textarea[name="msg"]').focus(function(){
            $alert.fadeOut('slow');
        });

        $form.find("form").ajaxForm({
            beforeSubmit: function(data, jqForm, options){
                var source = $(jqForm).find('input[name="source"]').val();
                var msg = $(jqForm).find('textarea[name="msg"]').val();
                var is_valid = validateVariables(source, msg);

                if(!is_valid){
                    $alert.show();
                    return false;
                } else {
                    $form.find('textarea').attr('disabled', 'disabled');
                    $form.find('input[type=submit]')
                        .attr('value', 'Saving ...')
                        .attr('disabled', 'disabled');
                    showLoading();
                    return true;
                }
            },

            success: function(responseText, statusText, xhr, jqForm){
                //console.log(JSON.stringify(responseText) + ", " + statusText);
                $form.find('textarea').removeAttr('disabled');
                $form.find('input[type="submit"]').attr('value', 'Save').removeAttr('disabled');

                $('#' + ID_SIDEBAR).find('.active').parent().removeClass('rosetta-inpage-todo');
                var nextId = $(jqForm).find('input[name="next"]').val();
                $('#' + nextId).trigger('click');
                hideLoading();
            }
        });
    }


    /**
     * Configure general events and controls
     */
    function initPage(){
        $('#' + ID_FORM).click(function(e){
            e.stopPropagation();
        });

        $('#' + ID_SIDEBAR).scroll(hideForm);
        $(document).click(hideForm);
    }


    /**
     *
     * @param [e]
     */
    function hideForm(e){
        $('#' + ID_FORM).hide();
        $('#' + ID_SIDEBAR + ' a').removeClass("active");
    }


    /**
     * This is a nifty trick to place the cursor at the end of the text when the onfocus event is triggered
     * onfocus="var val=this.value; this.value=''; this.value= val;"
     * http://stackoverflow.com/questions/511088/use-javascript-to-place-cursor-at-end-of-text-in-text-input-element
     *
     * @param obj
     */
    function moveCursorToEnd(obj){
        var value = obj.val(); //store the value of the element
        $(obj).focus().val(value);
    }


    function showLoading(){
        //$('#' + PREFIX + '-loading').fadeIn('slow');
        //$('#' + PREFIX + '-loading').fadeIn();
        $('#' + PREFIX + '-loading').show();
    }


    function hideLoading(){
        //$('#' + PREFIX + '-loading').fadeOut('slow');
        //$('#' + PREFIX + '-loading').fadeOut();
        $('#' + PREFIX + '-loading').hide();
    }


    var PATTERN = /%(?:\([^\s\)]*\))?[sdf]/g;

    function validateVariables(source, newbie){
        if(!source || !newbie){
            return false;
        }

        var matches_source = source.match(PATTERN);
        var matches_newbie = newbie.match(PATTERN);

        if(matches_source && matches_newbie && matches_source.length != matches_newbie.length){
            return false;
        } else if(matches_source || matches_newbie){
            return false;
        }

        return true;
    }







    /**
     *
     */
    Inpage.init = function(){
        initLinks();
        initForm();
        initPage();
    };

    Inpage.reload = function(){
        showLoading();
        window.location.reload();

//        var url = window.location;
//
//        $.get(url, function(data) {
//            data = data.replace(/<(\/)?body([^>]*)>/g, '<body>');
//            var indexBegin = data.indexOf('<body>');
//            var indexEnd = data.indexOf('<!--ROSETTA_INPAGE_BEGIN-->');
//            alert(indexBegin + ", " + indexEnd);
//            var s = data.substring(indexBegin+6, indexEnd);
//            console.log(s);
//            $('body').html(s);
//        });

        return false;
    };

    Inpage.github = function(){
        showLoading();
        $.post(ROOT + "/ajax/github", function(data){
            console.log(JSON.stringify(data));
        });
        setTimeout(hideLoading, 2000);
    };

    /**
     * Exposing functionality
     * Remapping Inpage to RosettaInpage
     */
    if(!window.RosettaInpage){
        window.RosettaInpage = Inpage;
    }
})(window, document);





//Deprecated
/*
$("span[contenteditable]").click(function(e){
    var text = $(this).html();
    var pos = $(this).position();
    var id = $(this).attr('id');

    console.log("Pos = " + JSON.stringify(pos) + ", " + id);
    $('#s-' + id).trigger('click');
    //$('#s-4a6a59aa75d28c79e8e9485d5019ddd9').trigger('click');
});

$("a").click(function(e){
    var id = $(this).attr('id');
    console.log("DDD = " + id);
    e.preventDefault();
});
*/



/*
//<!--
google.load("jquery", "1.3");



google.setOnLoadCallback(function() {
    $('.location a').show().toggle(function() {
        $('.hide', $(this).parent()).show();
    }, function() {
        $('.hide', $(this).parent()).hide();
    });



    $('td.plural').each(function(i) {
        var td = $(this), trY = parseInt(td.closest('tr').offset().top);
        $('textarea', $(this).closest('tr')).each(function(j) {
            var textareaY=  parseInt($(this).offset().top) - trY;
            $($('.part',td).get(j)).css('top',textareaY + 'px');
        });
    });

    $('.translation textarea').blur(function() {
        if($(this).val()) {
            $('.alert', $(this).parents('tr')).remove();
            var RX = /%(?:\([^\s\)]*\))?[sdf]/g,
                origs=$('.original', $(this).parents('tr')).html().match(RX),
                trads=$(this).val().match(RX),
                error = $('<span class="alert">Unmatched variables</span>');
            if (origs && trads) {
                for (var i = trads.length; i--;){
                    var key = trads[i];
                    if (-1 == $.inArray(key, origs)) {
                        $(this).before(error)
                        return false;
                    }
                }
                return true;
            } else {
                if (!(origs === null && trads === null)) {
                    $(this).before(error);
                    return false;
                }
            }
            return true;
        }
    });

    $('.translation textarea').eq(0).focus();

});
    */