/**
 * Created by HZ on 23-03-2015, 0023.
 */

function project_deploy(project_id, project_type, spinner, message){
    start_long_task(project_id, project_type, spinner, message);
}


function start_long_task(project_id, project_type, spinner, message) {
    $.ajax({
        type: 'POST',
        url: '/longtask',
        data: {
            project_id: project_id,
            project_type: project_type
        },
        success: function (data, status, request) {
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
        if (data['state'] != 'PENDING' && data['state'] != 'INITIAL' && data['state'] != 'PROGRESS') {
            $(spinner).hide();

            if ('result' in data) {
                $(message).text(data['status']);
                // show result
                $('<p class="btn btn-info"></p>').text('Result: ' + data['result']).appendTo('#deployment');
                $('div.panel-footer').hide();

            }
            else {
                // something unexpected happened
                $('<p class="btn btn-info"></p>').text('Result: ' + data['state']).appendTo('#deployment');
                $('div.panel-footer').hide();
            }

            // show the log in terminal window
            show_log(data);

        }
        else {
            $(message).text(data['status']);
            console.log(data);
            if ('cmd' in data){
                $('<p class="command"></p>').text('$~> ' + data['cmd']).appendTo('div.terminal');
                for (each in data['output']) {
                    $('<p class="output"></p>').text(data['output'][each]).appendTo('div.terminal');
                }
            }
            // rerun in 1-2 seconds
            setTimeout(function () {
                update_progress(status_url, spinner, message);
            }, 2000);
        }
    }
    );
}


function show_log(data){
    $('div.window').css('display', 'block');
    for (var i in data['log']) {
        if ($.isArray(data['log'][i][0])) {
            for (var j in data['log'][i]) {
                $('<p class="command"></p>').text('$~> ' + data['log'][i][j][0]).appendTo('div.terminal');
                for (var each in data['log'][i][j][1]) {
                    $('<p class="output"></p>').text(data['log'][i][j][1][each]).appendTo('div.terminal');
                }
            }
        }
        else {
            $('<p class="command"></p>').text('$~> ' + data['log'][i][0]).appendTo('div.terminal');
            for (var each in data['log'][i][1]) {
                $('<p class="output"></p>').text(data['log'][i][1][each]).appendTo('div.terminal');
            }
        }
    }
}