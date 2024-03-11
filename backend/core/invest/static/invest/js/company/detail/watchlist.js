import { slug } from "./consts.js";
import { getCookie } from "../../utils/utils.js";
import { sendNotification } from "../../base/notification.js";


let watchlistButtons = document.querySelectorAll('.button-watchlist')
let watchlistedButtons = document.querySelectorAll('.button-watchlisted')
let noteButtons

const sidebarButtons = document.querySelector('.d-sidebar__buttons')
const detailButtons = document.querySelector('.detail__buttons')

const watchlistButton = "" +
    "<button class=\"button-watchlist button text button--theme-bg-blue ml-4 pl-36\">\n" +
    "<svg class=\"svg button__svg\"><use href=\"#outline-star-icon\"></use></svg>\n" +
    "Add to watchlist\n" +
    "</button>"

const watchlistedButton = "" +
    "<button class=\"button-watchlisted button text button--theme-bg-blue ml-4\">\n" +
    "<svg class=\"svg button__svg button__svg--unique-object\"><use href=\"#star-solid-icon\"></use></svg>\n" +
    "</button>"

const noteButton = "" +
    "<button class=\"button-note button text button--theme-bg-blue ml-4 pl-36\">\n" +
    "<svg class=\"svg button__svg\">\n" +
    "<use href=\"#pen-icon\"></use>\n" +
    "</svg>\n" +
    "Add note\n" +
    "</button>"

if (watchlistButtons.length !== 0) {
    watchlistButtons.forEach(node => node.addEventListener('click', addCompanyToWatchlist))
}

if (watchlistedButtons.length !== 0) {
    watchlistedButtons.forEach(node => node.addEventListener('click', deleteCompanyFromWatchlist))
}

function addCompanyToWatchlist() {
    const origin = location.origin
    const url = `${origin}/watchlist/api/v1/toggle_watchlisted_company/`

    const csrfToken = getCookie('csrftoken')

    let data = new FormData()
    data.append('slug', slug)

    const options = {
        method: 'PATCH',
        body: data,
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
    }

    fetch(url, options)
        .then(response => {
            if (response.status === 201) {
                watchlistButtons = document.querySelectorAll('.button-watchlist')
                watchlistedButtons = document.querySelectorAll('.button-watchlisted')
                noteButtons = document.querySelectorAll('.button-note')

                // Трансформировать кнопку добавления to watchlist в кнопку удаления from watchlist
                watchlistButtons.forEach((node) => {node.remove()})
                // Добавить на страницу кнопку добавления заметок
                sidebarButtons.insertAdjacentHTML('afterbegin', noteButton)
                sidebarButtons.insertAdjacentHTML('afterbegin', watchlistedButton)

                detailButtons.insertAdjacentHTML('afterbegin', noteButton)
                detailButtons.insertAdjacentHTML('afterbegin', watchlistedButton)

                watchlistedButtons = document.querySelectorAll('.button-watchlisted')
                if (watchlistedButtons.length !== 0) {
                    watchlistedButtons.forEach(node => node.addEventListener('click', deleteCompanyFromWatchlist))
                }

                // Уведомить клиент о добавлении компании в Watchlist
                sendNotification('success', 'Компания успешно добавлена в Watchlist')
            }
        })
}

function deleteCompanyFromWatchlist() {
    const origin = location.origin
    const url = `${origin}/watchlist/api/v1/toggle_watchlisted_company/`

    const csrfToken = getCookie('csrftoken')

    let data = new FormData()
    data.append('slug', slug)

    const options = {
        method: 'DELETE',
        body: data,
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
    }

    fetch(url, options)
        .then(response => {
            if (response.status === 204) {
                let watchlistButtons = document.querySelectorAll('.button-watchlist')
                let watchlistedButtons = document.querySelectorAll('.button-watchlisted')
                let noteButtons = document.querySelectorAll('.button-note')

                // Трансформировать кнопку добавления to watchlist в кнопку удаления from watchlist
                watchlistedButtons.forEach((node) => {node.remove()})
                noteButtons.forEach((node) => {node.remove()})
                // Добавить на страницу кнопку добавления заметок
                sidebarButtons.insertAdjacentHTML('afterbegin', watchlistButton)
                detailButtons.insertAdjacentHTML('afterbegin', watchlistButton)

                watchlistButtons = document.querySelectorAll('.button-watchlist')
                if (watchlistButtons.length !== 0) {
                    watchlistButtons.forEach(node => node.addEventListener('click', addCompanyToWatchlist))
                }

                // Уведомить клиент об удалении компании из Watchlist
                sendNotification('success', 'Компания успешно удалена из Watchlist')
            }
        })
}
