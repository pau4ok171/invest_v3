// ...........................ВСПЛЫВАЮЩАЯ ФОРМА...........................

// ФОРМЫ
const initLoginForm = document.querySelector('.modal__menu--initLogin');
const loginForm = document.querySelector('.modal__menu--login');
const registerForm = document.querySelector('.modal__menu--register');
// Кнопка закрытия
const formCloseButtons = document.querySelectorAll('.login__close-button');
// Кнопки перехода
const initLoginOpenButton = document.querySelector('.modal__initLoginButton');
const loginOpenButtons = document.querySelectorAll('.modal__loginButton');
const registerOpenButtons = document.querySelectorAll('.modal__registerButton');
// Обёртка
const pageWrapper = document.querySelector('#root');


if (initLoginOpenButton) {
	initLoginOpenButton.addEventListener('click', openInitLoginForm);
}

function openInitLoginForm () {
	initLoginForm.classList.add('login--active');
	pageWrapper.style.filter = 'blur(6px)';
}

if (formCloseButtons) {
	formCloseButtons.forEach(function (node) {
		node.addEventListener('click', closeOpenedForm);
	});
}

function closeOpenedForm (event) {
	event.target.closest('.modal__menu').classList.remove('login--active');
	pageWrapper.style.filter = '';
}

if (loginOpenButtons) {
	loginOpenButtons.forEach(function (node) {
		node.addEventListener('click', openLoginForm);
	});
}

function openLoginForm (event) {
	loginForm.classList.add('login--active');
	closeOpenedForm (event);
	pageWrapper.style.filter = 'blur(6px)';
}

if (registerOpenButtons) {
	registerOpenButtons.forEach(function (node) {
		node.addEventListener('click', openRegisterForm);
	});
}

function openRegisterForm (event) {
	registerForm.classList.add('login--active');
	closeOpenedForm (event);
	pageWrapper.style.filter = 'blur(6px)';
}

// ...........................ОБРАБОТКА ФОРМЫ...........................

// Тег формы в логин-форме
const loginFormInputs = loginForm.querySelectorAll('input');
const registerFormInputs = registerForm.querySelectorAll('input');
const formInputs = [...loginFormInputs, ...registerFormInputs];
const errorMessage = `<div class="form__error">
							<span>Invalid email address</span>
							</div>`

// Добавить прослушку на inputs
formInputs.forEach(function (node) {
	node.addEventListener('blur', validInput);
});

formInputs.forEach(function (node) {
	node.addEventListener('input', checkForm);
});

// Проверять при действиях валидность формы
function validInput (event) {
	// Если валидно убрать код с ошибкой
	if (event.target.validity.valid) {
		resetError(event);
	// Если не валидно вставить код с ошибкой
	} else {
		showError(event);
	}
}

function checkForm (event) {
	if (event.target.validity.valid) {
		resetError(event);
	}

}

function resetError (event) {
	const formError = event.target.parentNode.querySelector('.form__error');
	if (formError) {
		event.target.classList.remove('form__input--error');
		formError.remove();
	}
}

function showError(event) {
	const formError = event.target.parentNode.querySelector('.form__error');
	if (!formError) {
		event.target.classList.add('form__input--error');
		event.target.parentNode.insertAdjacentHTML('beforeend', errorMessage);
	}
}

// ...........................АКТИВАЦИЯ КНОПКИ...........................
formInputs.forEach(function (node) {
	node.addEventListener('input', checkFormValidity);
});

function checkFormValidity(event) {
	let isValidCount = 0;
	let isValid = false;
	const inputs = event.target.closest('form').querySelectorAll('.form__input');

	inputs.forEach(function (node) {
		if (node.validity.valid) {
			isValidCount++;
		}
	});

	isValid = isValidCount === inputs.length

	validateForm(event, isValid);

}

// Разблокировать кнопку если форма валидна
function validateForm(event, isValid) {
	 const submitFormButton = event.target.closest('form').querySelector('.form__button');
	if(isValid) {
		submitFormButton.disabled = false;
		submitFormButton.classList.remove('form__button--disabled');
	} else {
		submitFormButton.disabled = true;
		submitFormButton.classList.add('form__button--disabled');
	}

}

// ...........................USER AUTHENTICATION...........................
const loginFormEL = document.querySelector('#login-form')
loginFormEL.addEventListener('submit', function (event) {
	event.preventDefault();
	const url = this.action
	const method = this.method
	const data = new FormData(this)
	const errorsEl = document.querySelector('.login-form__errors p')

	fetch(url, {
		method: method,
		body: data,
	})
		.then(response => {
			if (response.status === 400) {
				errorsEl.classList.add('form__errors--active')
				response.json().then(data => {errorsEl.textContent = data.error})
				return
			}

			if (response.status === 201) location.reload()
		})
		.catch(error => console.log(error))
})

// ...........................USER REGISTRATION...........................
const registerFormErrors = document.querySelector('.register-form__errors p')
const registrationForm = document.querySelector('#registration-form')

// Проверка доступности имени пользователя
document.querySelector('#registration_id_username').addEventListener('blur', verify_username)

function verify_username (event) {
	const target = event.target
	const value = target.value

	const url = registrationForm.action
	const method = registrationForm.method
	const csrf = registrationForm.querySelector('input[name="csrfmiddlewaretoken"]').value

	let body = new FormData()
	body.append('username', value)
	body.append('validate_username', true)
	body.append('csrfmiddlewaretoken', csrf)

	if (value) {
		fetch(url, {
			method: method,
			body: body,
			credentials: "same-origin",
		})
			.then(response => {
				if (response.status === 200) {
					response.json().then(data => {
						if (data.is_taken) {
							registerFormErrors.classList.add('form__errors--active')
							registerFormErrors.textContent = data.error
						} else {
							registerFormErrors.classList.remove('form__errors--active')
							registerFormErrors.textContent = null
						}
					})
				}
			})
			.catch(error => console.log(error))
	}
}

// Отправка формы регистрации на сервер
registrationForm.addEventListener('submit', registrateNewUser)
function registrateNewUser(event) {
	event.preventDefault();
	const url = this.action
	const method = this.method
	const data = new FormData(this)

	fetch(url, {
		method: method,
		body: data,
	})
		.then(response => {
			if (response.status === 201) {
				location.reload()
				return
			}

			if (response.status === 400) {
				response.json().then(data => {
					const errors = data.errors
					// Проверка на присутствие блока с ошибками
					if (errors) {
						// Пройтись по полям формы
						const inputs = registrationForm.querySelectorAll('input.form__input')
						inputs.forEach(node => {
							const fieldSetEl = node.parentNode
							const fieldError = fieldSetEl.querySelector('.form__field-error')
							// Проверить есть ли блок с ошибками
							if (fieldError)  fieldError.remove()

							fieldSetEl.insertAdjacentHTML('beforeend', '<div class="form__field-error"><ul></ul></div>')

							const errorsList = errors[node.name]
							console.log(errors, node.name, errorsList)
							if (errorsList) {
								errorsList.forEach(element => {
									fieldSetEl.querySelector('.form__field-error ul').insertAdjacentHTML('beforeend', `<li>${element}</li>`)
								})
							}
						})
					}
				})
			}
		})
}
