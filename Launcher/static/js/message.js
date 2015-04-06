/**
 * Created by HZ on 05-04-2015, 0005.
 */
function show_message(row) {
    $.ajax({
        type: 'POST',
        url: '/message',
        data: {msg_id: row.id },
        success: function (data) {
            $('p.sender').text(data['sender']);
            $('p.receiver').text(data['receiver']);
            $('span.date').text(data['date']);
            $('p.msg-body').text(data['msg-body']);
            $('#msg-read').modal('show');
            if (data['seen']) {
                $('tr#' + data['msg_id']).removeClass('bold');
                $('tr#' + data['msg_id'] + ' > td.inbox-read').html('<i class="glyphicon glyphicon-check"></i>');
            }

        },
        error: function () {
            alert('Unexpected error');
        }
    });
}