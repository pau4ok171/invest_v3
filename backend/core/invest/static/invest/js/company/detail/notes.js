import { Editor } from 'https://esm.sh/@tiptap/core'
import StarterKit from 'https://esm.sh/@tiptap/starter-kit'
import Placeholder from 'https://esm.sh/@tiptap/extension-placeholder'

Placeholder.configure({
  placeholder: ({ node }) => {
    if (node.type.name === 'heading') {
        return 'What’s the title?'
    }

    return 'Can you add some further context?'
  },
})


const editor = new Editor({
  element: document.querySelector('.notes_modal_menu__main'),
  onUpdate({ editor }) {
      console.log(editor.getHTML())
  },
  extensions: [
    StarterKit,
    Placeholder.configure({
        emptyEditorClass: 'is-editor-empty',
        placeholder: 'Write your thoughts, links, and company narrative'
    })
  ],
})

const notesModalMenu = document.querySelector('.notes_modal_menu')
const resizeButton = notesModalMenu.querySelector('.notes_modal_menu__button--resize')
const noteOpenButtons = document.querySelectorAll('.button-note')

noteOpenButtons.forEach(component => component.addEventListener('click', event => {
    if (!notesModalMenu.classList.contains('modal_menu--active')) {
        notesModalMenu.classList.add('notes_modal_menu--lateral')
        notesModalMenu.classList.add('modal_menu--active')
    }
}))

resizeButton.addEventListener('click', resizeNotesModalMenu)

function resizeNotesModalMenu(event) {
    notesModalMenu.classList.toggle('notes_modal_menu--lateral')
    const resizeUse = resizeButton.querySelector('use')
    resizeUse.setAttribute('href', resizeUse.getAttribute('href') === '#reduce-icon' ? '#expand-icon' : '#reduce-icon')
    document.body.toggleAttribute('disabled')
}

const boldButton = notesModalMenu.querySelector('.modal-menu__footer-button--bold')

boldButton.addEventListener('click', event => {
    if (editor.can().chain().focus().toggleBold().run()) {
        editor.chain().focus().toggleBold().run()
    }
})

const listButton = notesModalMenu.querySelector('.modal-menu__footer-button--list')

listButton.addEventListener('click', event => {
    if (editor.can().chain().focus().toggleBulletList().run()) {
        editor.chain().focus().toggleBulletList().run()
    }
})

