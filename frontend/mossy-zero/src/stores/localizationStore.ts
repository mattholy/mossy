import { defineStore } from 'pinia'
import { setI18nLanguage } from '@/i18n'
import { zhCN, dateZhCN } from 'naive-ui'
import { enUS, dateEnUS } from 'naive-ui'

interface LocalizationState {
    language: string;
}

export const useLocalizationStore = defineStore('localization', {
    state: (): LocalizationState => ({
        language: 'zh-CN',
    }),
    getters: {
        currentLanguageName(): string {
            return languageNames[this.language];
        },
        currentNaiveUILanguage(): any {
            return naiveUILanguage[this.language];
        },
        currentNaiveDateLanguage(): any {
            return naiveDateLanguage[this.language];
        }
    },
    actions: {
        setLanguage(language: string): void {
            this.language = language
            setI18nLanguage(language)
        },
    },
    persist: true,
});

const languageNames: { [key: string]: string } = {
    'zh-CN': '简体中文',
    'en-US': 'English',
};

const naiveUILanguage: { [key: string]: any } = {
    'zh-CN': zhCN,
    'en-US': enUS,
};

const naiveDateLanguage: { [key: string]: any } = {
    'zh-CN': dateZhCN,
    'en-US': dateEnUS,
};