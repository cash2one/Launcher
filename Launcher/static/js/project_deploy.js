/**
 * Created by HZ on 23-03-2015, 0023.
 */

$('#deploy').click(function() {
    $.getJSON('/task_execute', {
        cmd: 'dir'
    }, function (data) {
        $("span.cmd").text(data.cmd);
        for (each in data.output){
//            $("div.terminal").append('<p class="output">&nbsp&nbsp&nbsp'+ document.createTextNode(data.output[each]) +'</p>');
//            $("p.output").append(document.createTextNode(data.output[each]));
            $('<p class="output"></p>').text(data.output[each]).appendTo('div.terminal');
        }
    });
});
