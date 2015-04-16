    $(document).ready(function() {
        function newParameters(query) {
            query.instance = $('#id_actual_instance_1').val();
        }

        $('#id_actual_step_0').djselectable('option', 'prepareQuery', newParameters);
    });
