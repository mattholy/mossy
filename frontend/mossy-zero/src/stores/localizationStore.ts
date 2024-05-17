import { defineStore } from 'pinia';
import { setI18nLanguage } from '@/i18n'

interface LocalizationState {
    language: string;
}

export const useLocalizationStore = defineStore('localization', {
    state: (): LocalizationState => ({
        language: 'zh-CN',
    }),
    getters: {
        currentLanguage(): string {
            return languageNames[this.language];
        },
    },
    actions: {
        setLanguage(language: string): void {
            this.language = language
            setI18nLanguage(language)
        },
    },
});

const languageNames: { [key: string]: string } = {
    'zh-CN': '简体中文',
    'en-US': 'English',
};