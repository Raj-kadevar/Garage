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
    var url;
    if ($('#submit').text() == 'Add bike')
    {
        var url = "http://127.0.0.1:8000/add-bike/"
    }else{
        var url = "http://127.0.0.1:8000/add-car/"
    }
    carAjaxRequest('POST', csrfToken, url, formdata, function(response) {
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
           $('#mileage').text(response['mileage'])
        }
    })
    callbakc();
});
var url;
function update(id){
    url = "http://127.0.0.1:8000/update-car/"+id;
    ajaxGet('GET', url, function(response) {
        if (response.error) {
            alert('error');
        }
        else {
            $('.Name').val(response[0].fields['name']);
            $('.Color').val(response[0].fields['color']);
            $('.Price').val(response[0].fields['price']);
            $('.Mileage').val(response[0].fields['mileage']);
            $('.Plate').val(response[0].fields['plate_number']);
            $('.Image').val(response[0].fields['image']);
        }
    })
}

function updateBike(id){
    url = "http://127.0.0.1:8000/update-bike/"+id;
    ajaxGet('GET', url, function(response) {
        if (response.errors) {
            alert('error');
        }
        else {
            $('.Name').val(response[0].fields['name']);
            $('.Color').val(response[0].fields['color']);
            $('.Price').val(response[0].fields['price']);
            $('.Mileage').val(response[0].fields['mileage']);
            $('.Plate').val(response[0].fields['plate_number']);
            $('.Image').val(response[0].fields['image']);
        }
    })
}

function deleteBike(id){
    url = "http://127.0.0.1:8000/delete-bike/"+id;
    ajaxGet('GET', url, function(response) {
        if (response.message) {
            $('#bike').trigger('click');
        }
        else {
            alert('error');
        }
    })
}

function deleteCar(id){
    url = "http://127.0.0.1:8000/delete-car/"+id;
    ajaxGet('GET', url, function(response) {
        if (response.message) {
            $('#car').trigger('click');
        }
        else {
            alert('error');
        }
    })
}

$("#update_car").click(function(event){
    $('span').text('')
    event.preventDefault();
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formdata = new FormData();
    formdata.append('name',$('.Name').val());
    formdata.append('price',$('.Price').val());
    formdata.append('color',$('.Color').val());
    formdata.append('plate_number', $("input[name=number]").val());
    formdata.append('mileage',$('.Mileage').val());
    carAjaxRequest('POST', csrfToken, url, formdata, function(response) {
        if (response.message) {
           $('.btn-close').trigger('click');
           alert('successfully updated');
           if(response.message == 'successful')
           {
                $('#bike').trigger('click');
           }else{
                $('#car').trigger('click');
           }
        }
        else {
           $('#nm').text(response['name'])
           $('#prc').text(response['price'])
           $('#clr').text(response['color'])
           $('#nmb').text(response['plate_number'])
           $('#mlg').text(response['mileage'])
        }
    })
    callbakc();
});

