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
        var form = $('#' + ID_FORM);
        //form.find('textarea').attr('disabled', 'disabled');

        form.find("form").ajaxForm({
            beforeSubmit: function(data, jqForm, options){
                console.log("1=" + data);
                console.log("2=" + jqForm);
                console.log("3=" + options);
                $(jqForm).find('textarea').attr('disabled', 'disabled');
                $(jqForm).find('input[type=submit]').attr('value', 'Saving ...');
                showLoading();
            },
            success: function(responseText, statusText, xhr, jqForm){
                console.log(JSON.stringify(responseText) + ", " + statusText);
                $(jqForm).find('textarea').removeAttr('disabled');
                $(jqForm).find('input[type="submit"]').attr('value', 'Save');

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
        $('#' + ID_SIDEBAR).scroll(hideForm);

        $('#' + ID_FORM).click(function(e){
            e.stopPropagation();
        });

        $(document).click(function(e){
            //console.log($(e.target).is(".rosetta-inpage-form"));
            hideForm();
            //$('#' + ID_FORM).hide();
        });
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
