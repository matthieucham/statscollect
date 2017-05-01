$(document).ready(function () {
    function newParameters(query) {
        query.instance = $('#id_actual_instance_1').val();
        query.gamesheet = $('#id_gamesheet_ds_1').val();
    }

    $('input[id="id_rating_ds_0"]').djselectable('option', 'prepareQuery', newParameters);
});