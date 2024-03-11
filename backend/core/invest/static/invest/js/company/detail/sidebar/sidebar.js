const scrollVisible = 25
const scrollHidden = 200
const sidebar_header = document.querySelector('.d-sidebar__header')
const sidebar_body = document.querySelector('.d-sidebar__body')

window.addEventListener('scroll', () => {
    const opacity = get_opacity()
    change_opacity(opacity)
})

function get_opacity() {
    const scrollY = window.scrollY
    let opacity = 0

    if (scrollY < scrollHidden && scrollY > scrollVisible) {
        opacity = (scrollY - scrollVisible) /  (scrollHidden - scrollVisible)
        return opacity
    }

    if (scrollY <= scrollVisible) {
        opacity = 0
        return opacity
    }

    if (scrollY >= scrollHidden) {
        opacity = 1
        return opacity
    }

}

function change_opacity(opacity) {
    sidebar_header.style.setProperty('opacity', opacity)
    sidebar_body.style.setProperty('opacity', opacity)

    if (opacity === 0) {
        sidebar_header.style.setProperty('visibility', 'hidden')
        sidebar_body.style.setProperty('visibility', 'hidden')
    } else {
        sidebar_header.style.setProperty('visibility', 'visible')
        sidebar_body.style.setProperty('visibility', 'visible')
    }
}