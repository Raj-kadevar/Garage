$("#submit").click(function(event){
    $('span').text('')
    event.preventDefault();
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formdata = new FormData();
    formdata.append('name',$('#Name').val());
    formdata.append('price',$('#Price').val());
    formdata.append('color',$('#Color').val());
    formdata.append('plate_number', $("input[name=plate_number]").val());
    formdata.append('mileage',$('#Mileage').val());
    formdata.append('image', $('input[type=file]')[0].files[0]);

    carAjaxRequest('POST', csrfToken, "", formdata, function(response) {
        if (response.message) {
            $('#vehicle_form')[0].reset();
            alert('successfully added');
        }
        else {
           $('#name').text(response['name'])
           $('#price').text(response['price'])
           $('#color').text(response['color'])
           $('#image').text(response['image'])
           $('#number').text(response['plate_number'])
        }
    })

});