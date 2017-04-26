/**
 * Created by mgrandrie on 14/04/2017.
 */
(function ($) {
    /*$(document).ready(function () {
     function newParameters(query) {
     query.instance = $('#id_actual_instance_1').val();
     }

     $('input[id*="id_processedgameratingsource_set"]').djselectable('option', 'prepareQuery', newParameters);
     });*/

    function newParameters(query) {
        query.instance = $('#id_actual_instance_1').val();
    }

    $(document).on('formset:added', function (event, $row, formsetName) {
        if (formsetName == 'processedgameratingsource_set') {
            // Do something
            console.log('Do something');
            $row.find('input[id*="id_processedgameratingsource_set"]').djselectable('option', 'prepareQuery', newParameters);
        }
    });

    $(document).on('formset:removed', function (event, $row, formsetName) {
        // Row removed
    });
})(django.jQuery);