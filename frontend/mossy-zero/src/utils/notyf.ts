import { Notyf } from 'notyf'

export const notyf = new Notyf({
    duration: 10000,
    position: {
        x: 'right',
        y: 'top',
    },
    dismissible: true
})