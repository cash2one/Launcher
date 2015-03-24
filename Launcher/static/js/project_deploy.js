/**
 * Created by HZ on 23-03-2015, 0023.
 */

function project_deploy(project_id){
    var cmd_list = [];

    $.getJSON('/prism_deploy',{project_id:project_id},function(){alert('Success');})

//    $.getJSON('/task_execute', {
//        cmd: 'ls -l'
//    }, function (data) {
//        $('<p class="command"></p>').text('$~> ' + data.cmd).appendTo('div.terminal');
//        for (each in data.output) {
////            $("div.terminal").append('<p class="output">&nbsp&nbsp&nbsp'+ document.createTextNode(data.output[each]) +'</p>');
////            $("p.output").append(document.createTextNode(data.output[each]));
//            $('<p class="output"></p>').text(data.output[each]).appendTo('div.terminal');
//        }
//    });

}


