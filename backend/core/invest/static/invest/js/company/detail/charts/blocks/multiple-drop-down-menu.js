const chartBtns = document.querySelectorAll('.chart__tab-button')

chartBtns.forEach((el) => el.addEventListener('click', dropdownMenu))
window.addEventListener('click', (event) => {
    const activeDropMenus = document.querySelectorAll('.chart__dropdown-menu--active')
    activeDropMenus.forEach((el) => {
        el.classList.remove('chart__dropdown-menu--active')
    })
})

function dropdownMenu(event) {
    const target = event.target
    const activeDropMenus = document.querySelectorAll('.chart__dropdown-menu--active')

    activeDropMenus.forEach((el) => {
        if (el.parentNode === target.parentNode) return
        el.classList.remove('chart__dropdown-menu--active')
    })

    const droppableMenu = target.parentNode.querySelector('.chart__dropdown-menu')
    droppableMenu.classList.toggle('chart__dropdown-menu--active')
    event.stopPropagation()
}
