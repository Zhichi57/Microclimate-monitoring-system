$('#save_manual_button').on('click', function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        url: 'set_manual',
        method: 'post',
        headers: {'X-CSRFToken': csrftoken},
        data: {'manual_id': $('#select_manual').val()},
        success: function (data) {

        }
    });
});

$('#add_sensor_button').on('click', function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        url: 'add_sensor',
        method: 'post',
        headers: {'X-CSRFToken': csrftoken},
        data: $('#add_sensor_form').serialize(),
        success: function (data) {
            $('#add_sensor_form')[0].reset();
            $('#row_tbody_sensor').append(data);
        }
    });
});

function edit_sensor(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form = $('#edit_sensor_form_' + id);
    let data = {};
    $(form).find('input, textearea, select').each(function () {
        data[this.name] = $(this).val();
    });
    console.log(data);
    $.ajax({
        url: 'edit_sensor',
        method: 'post',
        headers: {'X-CSRFToken': csrftoken},
        data: form.serialize(),
        success: function () {
            $('#row_sensor_name_' + id).text(data.sensor_name);
            $('#row_sensor_api_key_' + id).text(data.api_key);
            $('#row_sensor_description_' + id).text(data.sensor_description);
        }
    });
}

function delete_sensor(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        url: 'delete_sensor',
        method: 'post',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            sensor_id: id,
        },
        success: function () {
            $('#row_sensor_' + id).hide();
        }
    });

}