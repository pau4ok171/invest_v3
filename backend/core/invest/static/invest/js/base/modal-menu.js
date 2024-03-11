const ModalMenuCloseButtons = document.querySelectorAll('.modal_menu__close-button')

ModalMenuCloseButtons.forEach(component => component.addEventListener('click', closeModalMenu))

function closeModalMenu (event) {
    event.target.closest('.modal_menu').classList.remove('modal_menu--active')
    document.body.removeAttribute('disabled')
}