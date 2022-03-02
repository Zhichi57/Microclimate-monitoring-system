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