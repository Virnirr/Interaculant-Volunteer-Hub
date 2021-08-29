
// AJAX scripts for taking in sign ups for services
function availability(id)
{
    var spots = document.getElementById(id);
    var avail = parseInt(spots.innerHTML) - 1;

    var server_data = [
        {"spots": avail, "server_id": id}
    ];


    $.ajax({
        type: "POST",
        url: "/availability",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',   
        success: function (result) {
            if(result.processed === "true") {
                window.location.reload(true);
                btn_id = "#" + id
                $(btn_id).html(avail);
                $(document).ready(function(){
                    $(window).scrollTop(0);
                });
            }

            else if(result.processed === "false") {
                window.location.reload(true);
                $(document).ready(function(){
                    $(window).scrollTop(0);
                });
            }
        }
    });
}

// AJAX scripts for removing joined services
function remove(service_id, user_id)
{
    var service_remove = [
        {"service_id": service_id, "user_id": user_id}
    ];
    $.ajax ({
        type: "POST",
        url: "/service_joined",
        data: JSON.stringify(service_remove),
        contentType: "application/json",
        dataType: 'json',  
        success: function (result) {
            if(result.processed === "true") {
                window.location.reload(true);
                $(document).ready(function(){
                $(window).scrollTop(0);
                });
            }
        }
    });
}