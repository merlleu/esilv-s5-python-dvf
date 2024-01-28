$(document).ready(function() {
    // if exclusive option is selected, disable all other selects

    // on page load
    $("select").each(function() {
        var selectedOption = $(this).find("option:selected");
        var optionExclusive = selectedOption.data("exclusive");
        if (optionExclusive) {
            $("select").not(this).prop("disabled", true);
        }
    });

    // on change
    $("select").change(function() {
        var selectedOption = $(this).find("option:selected");
        var optionExclusive = selectedOption.data("exclusive");
        if (optionExclusive) {
            $("select").not(this).prop("disabled", true);
        } else {
            $("select").prop("disabled", false);
        }
    });
    document.getElementById("loading-modal").style.display = "none";
});

function show_loading_modal() {
    document.getElementById("loading-modal").style.display = "flex";
}
