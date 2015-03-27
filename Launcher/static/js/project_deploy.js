/**
 * Created by HZ on 23-03-2015, 0023.
 */

function project_deploy(project_id, project_type, spinner, message){
    start_long_task(project_id, project_type, spinner, message);

//    $.getJSON('/prism_deploy',{project_id:project_id},function(){alert('Success');})

//    $.getJSON('/task_execute', {
//        cmd: 'ls -l'
//    }, function (data) {
//        $('<p class="command"></p>').text('$~> ' + data.cmd).appendTo('div.terminal');
//        for (each in data.output) {
//            $('<p class="output"></p>').text(data.output[each]).appendTo('div.terminal');
//        }
//    });
}


function start_long_task(project_id, project_type, spinner, message) {
    // add task status elements
    //div = $('<div><div></div><div>0%</div><div>...</div><div>&nbsp;</div></div><hr>');
    //spinner = $('<img src="/static/imgs/ajax-loader.gif" width="75" class="center-block"/>');
    $('#deployment').append(spinner);

    //message = $('<h3 class="well well-lg center-block">Status...</h3>');
    $('#deployment').append(message);

    // create a progress bar
//    var nanobar = new Nanobar({
//        bg: '#44f',
//        target: div[0].childNodes[0]
//    });

    // send ajax POST request to start background job
    $.ajax({
        type: 'POST',
        url: '/longtask',
        data: {project_id: project_id, project_type: project_type},
        success: function (data, status, request) {
            //alert('works');
            status_url = request.getResponseHeader('Location');
            update_progress(status_url, spinner, message);

        },
        error: function () {
            alert('Unexpected error');
        }
    });
}

function update_progress(status_url, spinner, message) {
    // send GET request to status URL
    $.getJSON(status_url, function (data) {
            //console.log(data);
        // update UI
        //percent = parseInt(data['current'] * 100 / data['total']);
        //nanobar.go(percent);
        //$(status_div.childNodes[1]).text(percent + '%');
        //$(status_div.childNodes[2]).text(data['status']);
        if (data['state'] != 'PENDING' && data['state'] != 'INITIAL' && data['state'] != 'PROGRESS') {
            $(spinner).hide();

            if ('result' in data) {
                $(message).text(data['status']);
                // show result
                //$(status_div.childNodes[3]).text('Result: ' + data['result']);
                $('<p class="btn btn-info"></p>').text('Result: ' + data['result']).appendTo('#deployment');
                $('div.panel-footer').hide();

            }
            else {
                // something unexpected happened
                //$(status_div.childNodes[3]).text('Result: ' + data['state']);
                $('<p class="btn btn-info"></p>').text('Result: ' + data['result']).appendTo('#deployment');
                $('div.panel-footer').hide();
            }
        }
        else {
            $(message).text(data['status']);
            // rerun in 1-2 seconds
            setTimeout(function () {
                update_progress(status_url, spinner, message);
            }, 1000);
        }
    }
    );
}