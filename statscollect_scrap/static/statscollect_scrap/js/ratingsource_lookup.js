    $(document).ready(function() {
        function newParameters(query) {
            query.instance = $('#id_actual_instance_1').val();
        }

        $('#id_processedgameratingsource_set-0-rating_source_0').djselectable('option', 'prepareQuery', newParameters);
        $('select[id*="id_processedgameratingsource_set"]').djselectable('option', 'prepareQuery', newParameters);
    });
