// ABOUT THE COMPANY
const aboutCompanyWrapper = document.querySelector('.about-company__description');
const aboutCompanyButton = aboutCompanyWrapper.querySelector('button');

const paragraphs = aboutCompanyWrapper.querySelectorAll('p');
let classedParagraphs = [];

paragraphs.forEach(function (node, index ) {
    node.classList.add(
        'text__p',
        'text__fw--n',
        'mb-24',
    )
    if (index === 0) {
        node.classList.add(
            'text__max2lines',
            'text__overflow-hidden'
        )
    } else {
        node.remove();
    }

    classedParagraphs.push(node);

});

aboutCompanyButton.addEventListener('click', function (event) {
    const target = event.target
    const parent = target.parentNode

    // remove all paragraphs from button's parent node
    parent.querySelectorAll('p').forEach(function (node) {
        node.remove()
    });

    // remove class lists hiding first paragraph
    classedParagraphs[0].classList.toggle('text__max2lines')
    classedParagraphs[0].classList.toggle('text__overflow-hidden')

    // If button is activate yet
    if (target.dataset.active === 'true') {

        // insert first paragraph in button's parent node
        parent.insertBefore(classedParagraphs[0], target)

        // change button
        target.dataset.active = 'false'
        target.innerText = 'Show more'
    }
    // if button is not activated yet
    else {

        // insert paragraphs in button's parent node
        classedParagraphs.forEach(function (node) {
            parent.insertBefore(node, target)
        });

        // change button
        target.dataset.active = 'true'
        target.innerText = 'Show less'

    }
})
// END ABOUT THE COMPANY

// ANALYST SOURCES
const analystSourcesOpenButton = document.querySelector('.analyst_sources_open_button')
const analystSourcesModalMenu = document.querySelector('.analyst_sources_modal_menu')

if (analystSourcesOpenButton) {
    analystSourcesOpenButton.addEventListener('click', (component) => {
        analystSourcesModalMenu.classList.add('modal_menu--active')
        document.body.setAttribute('disabled', '')
    })
}