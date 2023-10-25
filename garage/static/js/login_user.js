$("#close").click(function(){
  $(".message").hide();
});

$("#submit").click(function(event){
    $('span').text('')
    event.preventDefault();
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formdata = $("#login_form").serialize();
    makeAjaxRequest('POST', csrfToken, "", formdata, function(response) {
        if (response.error) {
           $('#error').text(response['error'])
        }
        else {
            window.location.href= '/index/';
        }
    })

});