import {getCookie} from "../../utils/utils.js";
import {slug} from "./consts.js";
import {sendNotification} from "../../base/notification.js";

const addToPortfolioButton = document.querySelector('.add_to_portfolio_open_button')
const addToPortfolioModalMenu = document.querySelector('.add_to_portfolio_modal_menu')

if (addToPortfolioButton) {
    addToPortfolioButton.addEventListener('click', (event) => {
        addToPortfolioModalMenu.classList.add('modal_menu--active')
    })
}

//Добавить в портфель
const addToPortfolioButtons = addToPortfolioModalMenu.querySelectorAll('.add_to_portfolio_modal_menu__button--add')
// Удалить из портфеля
const deleteFromPortfolioButtons = addToPortfolioModalMenu.querySelectorAll('.add_to_portfolio_modal_menu__button--delete')

if (deleteFromPortfolioButtons) {
   deleteFromPortfolioButtons.forEach(component => component.addEventListener('click', event => {
        processPortfolioButton(event, 'DELETE')
    }))
}
if (addToPortfolioButtons) {
    addToPortfolioButtons.forEach(component => component.addEventListener('click', event => {
        processPortfolioButton(event, 'PATCH')
    }))
}

// ОБРАБОТАТЬ КНОПКИ В МОДАЛЬНОМ МЕНЮ
const addToPortfolioButtonEl = "" +
    "<button class=\"add_to_portfolio_modal_menu__button add_to_portfolio_modal_menu__button--add\">\n" +
    "<svg height=\"20\" width=\"20\" viewBox=\"0 0 512 512\" fill=\"#fff\">\n" +
    "<use href=\"#add-icon\"></use>\n" +
    "</svg>\n" +
    "Add\n" +
    "</button>"

const addedToPortfolioButtonEl = "" +
    "<button disabled class=\"add_to_portfolio_modal_menu__button add_to_portfolio_modal_menu__button--added\">\n" +
    "<svg height=\"24\" width=\"24\" viewBox=\"0 0 24 24\" fill=\"#fff\">\n" +
    "<use href=\"#checked-icon\"></use>\n" +
    "</svg>\n" +
    "Added\n" +
    "</button>"

const deleteFromPortfolioButtonEl = "" +
    "<button class=\"add_to_portfolio_modal_menu__button add_to_portfolio_modal_menu__button--delete\">\n" +
    "<svg height=\"20\" width=\"20\" viewBox=\"0 0 512 512\" fill=\"#fff\">\n" +
    "<use href=\"#trash-icon\"></use>\n" +
    "</svg>\n" +
    "</button>"

const createNewPortfolioInputEl = "<input type='text' placeholder='Например: Мой новый портфель' class=\"add_to_portfolio_modal_menu__input\">"

function processPortfolioButton(event, method) {
    // Найти ближайший портфель
    const portfolioItem = event.target.closest('.add_to_portfolio_modal_menu__item')
    // Извлечь id портфеля
    const portfolioId = portfolioItem.dataset.id
    // Отправить запрос по api на добавление компании в портфель (Вернуть новые данные по портфелю)
    const url = `${location.origin}/portfolio/api/v1/portfolio_positions/`
    const csrfToken = getCookie('csrftoken')
    let data = new FormData()
    data.append('portfolio_id', portfolioId)
    data.append('company_slug', slug)

    const options = {
        method: method,
        body: data,
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin',
    }

    fetch(url, options)
        .then(response => response.json())
        .then(data => {
            const totalSharesBlock = portfolioItem.querySelector('.add_to_portfolio_modal_menu__info-block-total-shares')
            const addToPortfolioActionBlock = portfolioItem.querySelector('.add_to_portfolio_modal_menu__action-block')
            const plural =  data.total_positions > 1  ? 's' : ''
            totalSharesBlock.textContent = `${data.total_positions} Holding${plural} `
            // Обновить кнопки
            const portfolioButtons = portfolioItem.querySelectorAll('.add_to_portfolio_modal_menu__button')
            // Удалить кнопки из объекта портфеля
            portfolioButtons.forEach(node => node.remove())
            if (data.status === 201) {
                addToPortfolioActionBlock.insertAdjacentHTML('afterbegin', deleteFromPortfolioButtonEl)
                addToPortfolioActionBlock.insertAdjacentHTML('afterbegin', addedToPortfolioButtonEl)
                // Уведомить об удалении из портфеля
                sendNotification('success', 'Компания добавлена в Портфель')
            }
            if (data.status === 204) {
                addToPortfolioActionBlock.insertAdjacentHTML('afterbegin', addToPortfolioButtonEl)
                // Уведомить об удалении из портфеля
                sendNotification('success', 'Компания удалена из Портфеля')
            }
            addListenersToPortfolioButtons(portfolioItem)
        })
        .catch(error => console.log(error))
}

function addListenersToPortfolioButtons (portfolioItem) {
    //Добавить в портфель
    const addButtons = portfolioItem.querySelectorAll('.add_to_portfolio_modal_menu__button--add')
    // Удалить из портфеля
    const deleteButtons = portfolioItem.querySelectorAll('.add_to_portfolio_modal_menu__button--delete')

    if (deleteButtons) {
       deleteButtons.forEach(component => component.addEventListener('click', event => {
            processPortfolioButton(event, 'DELETE')
        }))
    }
    if (addButtons) {
        addButtons.forEach(component => component.addEventListener('click', event => {
            processPortfolioButton(event, 'PATCH')
        }))
    }
}
// END ОБРАБОТАТЬ КНОПКИ В МОДАЛЬНОМ МЕНЮ

// ДОБАВЛЕНИЕ НОВОГО ПОРТФЕЛЯ
const createNewPortfolioButton = addToPortfolioModalMenu.querySelector('.add_to_portfolio_modal_menu__button--new')
const modalMenuFooter = addToPortfolioModalMenu.querySelector('.add_to_portfolio_modal_menu__footer')
const PortfolioItemsBlock = addToPortfolioModalMenu.querySelector('.add_to_portfolio_modal_menu__main')
createNewPortfolioButton.addEventListener('click', (event) => {
    const target = event.target
    // Заменить кнопку на input
    target.remove()
    modalMenuFooter.insertAdjacentHTML('beforeend', createNewPortfolioInputEl)
    modalMenuFooter.lastElementChild.focus()
    const createNewPortfolioInput = modalMenuFooter.querySelector('.add_to_portfolio_modal_menu__input')
    createNewPortfolioInput.addEventListener('keydown', event => {
        if (event.code === 'Enter' && event.target.value) {
            // Создать портфель
                const url = `${location.origin}/portfolio/api/v1/create_portfolio/`
                const csrfToken = getCookie('csrftoken')
                let data = new FormData()
                data.append('name', event.target.value)

                const options = {
                    method: 'POST',
                    body: data,
                    headers: {'X-CSRFToken': csrfToken},
                    mode: 'same-origin',
                }

                fetch(url, options)
                    .then(response => response.json())
                    .then(data => {
                        // Прорисовать новый портфель в списке
                        const portfolioItemElement = createPortfolioItemElement(data)
                        PortfolioItemsBlock.insertAdjacentHTML('beforeend', portfolioItemElement)
                        // Добавить прослушку на кнопки
                        addListenersToPortfolioButtons(PortfolioItemsBlock.lastElementChild)

                        // Вернуть кнопку
                        event.target.remove()
                        modalMenuFooter.insertAdjacentElement('beforeend', createNewPortfolioButton)
                    })
        }
        else if (event.code === 'Escape') {
            // Вернуть кнопку
            event.target.remove()
            modalMenuFooter.insertAdjacentElement('beforeend', createNewPortfolioButton)
        }
    })

})

function createPortfolioItemElement(data) {
    const total_positions = data.positions.length
    const plural = total_positions ? 's' : ''

    const element = `` +
        `<div data-id="${data.id}" class="add_to_portfolio_modal_menu__item">\n` +
        `<div class="add_to_portfolio_modal_menu__info-block">\n` +
        `<div class="add_to_portfolio_modal_menu__info-block-title">${data.name}</div>\n` +
        `<div class="add_to_portfolio_modal_menu__info-block-total-shares">\n` +
        `${data.positions.length} Holding${plural}\n` +
        `</div>\n` +
        `</div>\n` +
        `\n` +
        `<div class="add_to_portfolio_modal_menu__action-block">\n` +
        `<button class="add_to_portfolio_modal_menu__button add_to_portfolio_modal_menu__button--add">\n` +
        `<svg height="20" width="20" viewBox="0 0 512 512" fill="#fff">\n` +
        `<use href="#add-icon"></use>\n` +
        `</svg>\n` +
        `Add\n` +
        `</button>\n` +
        `</div>\n` +
        `</div>`

    return element
}