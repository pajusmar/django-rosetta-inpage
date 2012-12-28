/**
 * Work in progress!
 *
 **/

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
    e.preventDefault();
});
