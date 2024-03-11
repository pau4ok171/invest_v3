const navSearchBlock = document.querySelector('.navigation__nav-search')
const navSearch = navSearchBlock.querySelector('.nav-search__input')
const navCrossIcon = navSearchBlock.querySelector('.nav-search__postfix-icon')

const navDropdown = navSearchBlock.querySelector('.nav_search__dropdown')

const navDropdownList = navDropdown.querySelector('.nav-search__dropdown-list')
const navDropdownItem = navDropdown.querySelector('.nav-search__dropdown-item')

navDropdownItem.remove()

// Настроить Reset Button
navSearch.addEventListener('input', function (event) {
    navCrossIcon.classList.remove('none')
    checkIfEmpty(event)
    event.stopPropagation()
})

function checkIfEmpty(event) {
    const value = event.target.value
    if (value.length === 0) {
        navCrossIcon.classList.add('none')
        return
    }
    search_result(value)
}

// Отчистить input
navCrossIcon.addEventListener('click', function (event) {
    navSearch.value = ''
    navSearch.focus()
})

function search_result(value) {
    fetch(`http://127.0.0.1:8000/invest/api/v1/search/?q=${value.toLowerCase()}`)
        .then(response => {return response.json()})
        .then(data => {createDropdownList(data)})
        .catch(err => {console.log(err)})
}

function createDropdownList(data) {
    disable_dropdown()

    if(data.length === 0) {return}

    // Отобразить меню
    navDropdown.classList.remove('none')
    data.forEach((el) => {
        const newItem = navDropdownItem.cloneNode(true)
        const navDropdownLink = newItem.querySelector('.nav-search__dropdown-link')
        const navDropdownLinkIcon = newItem.querySelector('.nav-search__dropdown-link-icon')
        const navDropdownTitle = newItem.querySelector('.nav-search__dropdown-title')
        const navDropdownMarketImg = newItem.querySelector('.nav-search__dropdown-market-img')
        const navDropdownMarketTitle = newItem.querySelector('.nav-search__dropdown-market-title')
        const navDropdownSector = newItem.querySelector('.nav-search__dropdown-sector')

        navDropdownLink.setAttribute('href', el.absolute_url)
        navDropdownLinkIcon.setAttribute('src', el.logo)
        navDropdownTitle.innerText = el.title
        navDropdownMarketTitle.innerText = `${el.market.title}:${el.ticker}`
        navDropdownSector.innerText = el.sector.title

        navDropdownList.append(newItem)
    })
}

function disable_dropdown() {
    // Выключить выпадающее меню
    navDropdown.classList.add('none')
    // Удалить все элементы из листа
    const navDropdownElements = navDropdownList.querySelectorAll('.nav-search__dropdown-item')
    navDropdownElements.forEach((el) => {el.remove()})
}

window.addEventListener('click', (event) => {
    disable_dropdown()
})

