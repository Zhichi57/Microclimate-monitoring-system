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


$('#select_date_button').on('click', function () {
    let start_date = $('#start_date').val();
    let end_date = $('#end_date').val();
    if ((start_date !== '') && (end_date !== '')) {
         window.location.href = "/?start_date=" + start_date + '&end_date=' + end_date;
    }

})

$( document ).ready(function() {
    let searchParams = new URLSearchParams(window.location.search)
    let start_date = searchParams.get('start_date')
    let end_date = searchParams.get('end_date')
    $('#start_date').val(start_date);
    $('#end_date').val(end_date);
});

$('#get_pdf_report').on('click', function () {
    let start_date = $('#start_date').val();
    let end_date = $('#end_date').val();
    if ((start_date !== '') && (end_date !== '')) {
         window.location.href = "pdf_report?start_date=" + start_date + '&end_date=' + end_date;
    }else {
        window.location.href = "pdf_report"
    }

})

$('#get_csv_report').on('click', function () {
    let start_date = $('#start_date').val();
    let end_date = $('#end_date').val();
    if ((start_date !== '') && (end_date !== '')) {
         window.location.href = "csv_report?start_date=" + start_date + '&end_date=' + end_date;
    }else {
        window.location.href = "csv_report"
    }

})
global_row_id = null;
$(document).ready(function () {
    setInterval(function () {
        let row_id;
        if (global_row_id === null) {
            row_id = $('#sensor_values_table tr:nth-child(1)')[1].id.replace('sensor_values_row_','');
        } else {
            row_id = global_row_id;
        }
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({
            url: 'update_values',
            method: 'post',
            headers: {'X-CSRFToken': csrftoken},
            data: {
                row_id: row_id,
            },
            success: function (data) {
                if (data.status === 'warning') {
                    $('#values_warning_modal').modal('show');
                    global_row_id = data.row_id
                }
            }
        });

    }, 5000);
});
