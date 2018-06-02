
/**
 * Note: requires jQuery!
 *
 * This will allow us to initialize a modal functionality
 * by just calling it with the trigger"s id and the target
 * id of the modal.
 */
function initModal(trigger, target) {
    $(document).ready(function () {
        $(trigger).on("click", function () {
            $(target).css("display", "block");
            $(`${target} .close`).on("click", function () {
                $(target).css("display", "none");
            });

            /* temporary to allow closing of modals by pressing submit */
            $(`${target} .bt-orange, ${target} .bt-red`).on("click", function () {
                $(target).css("display", "none");
            });
        });
    });
}
