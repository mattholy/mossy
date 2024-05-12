import { Notyf } from 'notyf'

export const notyf = new Notyf({
    duration: 5000,
    position: {
        x: 'right',
        y: 'top',
    },
    dismissible: true
})