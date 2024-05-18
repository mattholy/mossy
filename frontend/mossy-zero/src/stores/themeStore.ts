import { defineStore } from 'pinia'
import { useOsTheme } from 'naive-ui'

interface ThemeState {
    isDarkMode: boolean;
}

const osThemeRef = useOsTheme()
export const useThemeStore = defineStore('theme', {
    state: (): ThemeState => ({
        isDarkMode: osThemeRef.value === 'dark' ? true : false
    }),
    actions: {
        toggleDarkMode() {
            this.isDarkMode = !this.isDarkMode;
        },
        setDarkMode(isDarkMode: boolean) {
            this.isDarkMode = isDarkMode;
        }
    },
    persist: true
});
