// ...........................ВЫПАДАЮЩИЙ СПИСОК...........................

// Найти элементы
const accountMenu = document.querySelector('.account-access__dropdown');
const accountAccessButton = document.querySelector('.account-access__button');

if (accountAccessButton) {
	accountAccessButton.addEventListener('click', openAccountMenu);
}

window.addEventListener('click', closeAccountMenu);

function openAccountMenu() {
	accountMenu.removeAttribute('style')
	accountMenu.classList.toggle('account-access__dropdown--active');
}

function closeAccountMenu (event) {
	const target = event.target
	if (!target.closest('.account-access-dropdown') && !target.closest('.account-access__button')) {
		accountMenu.classList.remove('account-access__dropdown--active');
	}
}