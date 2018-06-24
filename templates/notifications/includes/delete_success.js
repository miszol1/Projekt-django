var deleteSuccess = function (response, notification) {
    //console.log(response);
    var $selected_notification = notification.closest(nfClassSelector);
    if (response.success) {
        $selected_notification.fadeOut(300, function () {
            $(this).remove()
        });
    }
};
