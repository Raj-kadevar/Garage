function makeAjaxRequest(methodType, csrfToken, url, data, callback)
{
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
