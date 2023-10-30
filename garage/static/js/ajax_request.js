function makeAjaxRequest(methodType, csrfToken, url, data, callback)
{
    debugger;
    $.ajax({
        method: methodType,
        headers: {
            'X-CSRFToken': csrfToken
        },
        url: url,
        data: data,
        success: function (data) {
            if (callback) {
                callback(data)
            }
        },
        error: function (data) {
             if (callback) {
                callback(data)
            }
        },

    });
}

function ajaxGet(methodType, url, callback) {
    $.ajax({
        method: methodType,
        url: url,
        contentType: false,
        success: function (data) {
            if (callback) {
                callback(data)
            }
        },

    });
}