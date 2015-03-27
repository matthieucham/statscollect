    $(document).ready(function() {
        function newParameters(query) {
            query.instance = $('#id_actual_instance').val();
        }

        $('#id_actual_step_0').djselectable('option', 'prepareQuery', newParameters);
    });
