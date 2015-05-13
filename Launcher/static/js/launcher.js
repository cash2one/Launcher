/**
 * Created by HZ on 13-05-2015, 013.
 */
$('div#credits').hide();
$('div#docs').hide();

$('button#show-credits').click(function (){
    $('div#credits').toggle();
});

$('button#show-docs').click(function (){
    $('div#docs').toggle();
});