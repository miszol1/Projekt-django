var markSuccess = function (response, notification) {
    //console.log(response);
    var unreadNotificationsCountHolder = $(unreadNotificationsCountSelector);
    var unreadNotificationsCount = Number(unreadNotificationsCountHolder.text());
    if (response.action == 'read') {
        var mkClass = readNotificationClass;
        var rmClass = unreadNotificationClass;
        unreadNotificationsCountHolder.text(unreadNotificationsCount-1);
        var action = 'unread';
    } else {
        mkClass = unreadNotificationClass;
        rmClass = readNotificationClass;
        unreadNotificationsCountHolder.text(unreadNotificationsCount+1);
        action = 'read';
    }
    // console.log(notification.closest(nfClassSelector));
    notification.closest(nfSelector).removeClass(rmClass).addClass(mkClass);
    notification.attr('data-mark-action', action);

    toggle_text = notification.attr('data-toggle-text') || 'Mark as ' + action;
    notification.attr('data-toggle-text', notification.html());
    notification.html(toggle_text);
};
