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

$("#close").click(function(){
  $(".message").hide();
});

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
