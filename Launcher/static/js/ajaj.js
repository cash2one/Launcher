/**
 * Created by HZ on 23-03-2015, 0023.
 */


//    $.ajax({
//        //type: "POST",
//        url: "/send",
//        data: {
//            a: $('input[name="a"]').val(),
//            b: $('input[name="b"]').val()
//        },
//        contentType: 'application/json;charset=UTF-8',
//        success: function (data) {
//            $("span.result").text(data.res);
////            $("span.result").html(data.res);
//            }
//
//    });
$('button.calculate').click(function () {
    $.getJSON('/send', {
        a: $('input[name="a"]').val(),
        b: $('input[name="b"]').val()
    }, function (data) {
        $("span.result").text(data.res);
    });

});

