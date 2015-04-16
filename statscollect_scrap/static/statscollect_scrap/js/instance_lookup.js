    $(document).ready(function() {
        function newParameters(query) {
            query.tournament = $('#id_actual_tournament').val();
        }

        $('#id_actual_instance_0').djselectable('option', 'prepareQuery', newParameters);
    });
