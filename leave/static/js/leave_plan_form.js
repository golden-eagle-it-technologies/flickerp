$(document).ready(() => {
    // Getting Leave Plan number of days
    $("#end_date").change(() => {
        start_date = document.querySelector('#start_date').value;
        end_date = document.querySelector('#end_date').value;

        $.ajax({
            type: 'get',
            url: configuration['leave']['get_number_of_days_between_two_dates'],
            data: { 'start_date': start_date, 'end_date': end_date },
            dataType: 'json',
            success: (data) => {
                if (data.success) {
                    document.querySelector('#number_of_days').value = data.number_of_days;
                } else {
                     alert("Something went wrong");
                }

            },

        });
    });
});