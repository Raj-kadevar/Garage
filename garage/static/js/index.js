function body(){
      var today = new Date();
      var time = today.getHours();
      if (time < 12){
        $('#header').text("Good morning");
      }
      else if(time < 16){
        $('#header').text("Good afternoon");
      }
      else{
        $('#header').text("Good evening");
      }
}

$("#bike").click(function(event){
    event.preventDefault();
    ajaxGet('GET', "http://127.0.0.1:8000/bike-list/", function(response) {
        if (response.error) {
            alert('error');
        }
        else {
            $('#main_block').html(response.page);
        }
    })
    Callback();
});

$("#car").click(function(event){
    event.preventDefault();
    ajaxGet('GET', "http://127.0.0.1:8000/car-list/", function(response) {
        if (response.error) {
            alert('error');
        }
        else {
            $('#main_block').html(response.page);
        }
    })
    Callback();
});

function repair(){
    ajaxGet('GET', "http://127.0.0.1:8000/repair-vehicle/", function(response) {
        if (response.error) {
            alert('error');
        }
        else {
            $('#main_block').html(response.page);
        }
    })
    Callback();
}


$("#repairVehicle").click(function(event){
    $('span').text('')
    event.preventDefault();
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formdata = new FormData();
    formdata.append('date',$('#id_date').val());
    formdata.append('type',$('#id_type').val());
    carAjaxRequest('POST', csrfToken, "http://127.0.0.1:8000/repair-vehicle/", formdata, function(response) {
        if (response.date) {
           $('#date').text(response['date'])
           $('#type').text(response['type'])
        }
        else {
           $('#main_block').html(response.page);
        }
    })
    Callback();
});

$("#book").click(function(event){
    $('span').text('')
    event.preventDefault();
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formdata = new FormData();
    formdata.append('slot',$('input[name="example"]:checked').val());
    carAjaxRequest('POST', csrfToken, "http://127.0.0.1:8000/book-slot/", formdata, function(response) {
        if (response.error) {
          alert('error');
        }
        else {
          alert('Booked');
          $('#bike').trigger('click');
        }
    })
    Callback();
});

