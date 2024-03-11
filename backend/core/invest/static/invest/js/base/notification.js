export function sendNotification(type, message) {
	const types = {
		success: {
			iconHref: 'checkmark-circle-icon',
			iconColor: '2dc97e',
		}
	}

	const typeOpts = types[type]

	let component = document.createElement('div')
	let componentInner = document.createElement('div')
	let componentIcon = document.createElement('div')
	let componentText = document.createElement('div')

	componentIcon.innerHTML = `<svg width="24" height="24" fill="#${typeOpts.iconColor}"><use href="#${typeOpts.iconHref}"></use></svg>`
	componentText.textContent = message

	component.className = 'snackbar'
	componentInner.className = 'snackbar__inner'
	componentIcon.className = 'snackbar__icon'
	componentText.className = 'snackbar__text'
	componentInner.appendChild(componentIcon)
	componentInner.appendChild(componentText)
	component.appendChild(componentInner)
	document.body.appendChild(component)

	setTimeout(() => component.classList.add('snackbar--active'), 5)
	setTimeout(() => component.classList.remove('snackbar--active'), 2200)
	setTimeout(() => component.remove(), 3000)
}