/// <reference path="jquery-3.6.0.js" />

$("button[name = 'alert_time_button']").on('click',()=>{
    // $('.list-sort').attr('colspan', (_, attr) => attr == 6 ? null : 6));
    $("input[name = 'alert_time']").attr('disabled',(_, attr) => {attr == 6 ? null : 6});
});