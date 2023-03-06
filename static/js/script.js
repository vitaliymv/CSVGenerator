const range_appear = (column_type) => {
    let row = $(column_type).parents(".form-inline")
    let from = $(row).find("[id$='range_from']")
    let to = $(row).find("[id$='range_to']")
    if ($(column_type).val() === "Text" || $(column_type).val() === "Integer") {
        $(from).show()
        $(to).show()
    } else {
        $(from).hide()
        $(to).hide()
    }
}

$(document).ready(function () {
    $('#add_column').click(function () {
        let form_idx = $('#id_column_set-TOTAL_FORMS').val();
        $('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
        $('#id_column_set-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });
    $("[id$='column_type']").each(
        function () {
            range_appear($(this))
        }
    )

    $("[id$='column_type']").change(
        (e) => {
            range_appear(e.target)
        }
    )
});