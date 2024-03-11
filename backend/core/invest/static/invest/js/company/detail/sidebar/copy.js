import { sendNotification } from "../../../base/notification.js";

const notifButton = document.querySelector('.d-sidebar__copy')
notifButton.addEventListener('click', addToClipBoard)

function addToClipBoard(event) {
    const pageLink = location.href
    navigator.clipboard.writeText(pageLink)
        .then(() => {
            sendNotification('success', 'Link Copied')
        })
        .catch(err => {console.log(err)})
}