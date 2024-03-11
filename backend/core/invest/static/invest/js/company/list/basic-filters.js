// ...........................BASIC FILTERS...........................
// Найти все dropdown buttons на странице
const dropdownBtns = document.querySelectorAll('.dropdown-button')

dropdownBtns.forEach((node) => {node.addEventListener('click', dropDownMenu)})

window.addEventListener('click', (event) => {
	const droppedMenus = document.querySelectorAll('.dropdown-menu--active')
	droppedMenus.forEach((node) => {
		node.classList.remove('dropdown-menu--active')
	})
})

function dropDownMenu(event) {
	const target = event.target
	const droppedMenus = document.querySelectorAll('.dropdown-menu--active')
	const droppedContainer =  target.closest('.dropdown-container')

	// Закрыть все открытые dropDownMenu кроме текущего
	droppedMenus.forEach((node) => {
		if (node.parentNode === droppedContainer) return
		node.classList.remove('dropdown-menu--active')
	})

	const currentMenu = target.parentNode.parentNode.querySelector('.dropdown-menu')
	currentMenu.classList.toggle('dropdown-menu--active')

	event.stopPropagation()
}

const dropdownContainers =  document.querySelectorAll('.dropdown-container')
dropdownContainers.forEach((node) => {node.addEventListener('click', (event) => {
	event.stopPropagation()
})})

// TODO: Добавить поиск для фильтров