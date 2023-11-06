

$("#submit").click(function(event){
    $('span').text('')
    event.preventDefault();
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formdata = $("#register_form").serialize();
    debugger;
    makeAjaxRequest('POST', csrfToken, "", formdata, function(response) {
        if (response.message) {
            window.location.href= '/login/';
        }
        else {
           $('#name').text(response['username'])
           $('#email').text(response['email'])
           $('#password1').text(response['password1'])
           $('#password2').text(response['password2'])
        }
    })

});