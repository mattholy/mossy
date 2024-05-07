import { createI18n } from 'vue-i18n'



async function loadLocaleMessages(locale: string) {
    const messages = await import(`./locales/${locale}.json`)
    return messages.default
}

const i18n = createI18n({
    legacy: false,
    locale: 'zh-CN',
    fallbackLocale: 'zh-CN',
    globalInjection: true,
    messages: {}
});


export async function setI18nLanguage(locale: string) {
    if (!i18n.global.availableLocales.includes(locale)) {
        const messages = await loadLocaleMessages(locale);
        i18n.global.setLocaleMessage(locale, messages);
    }
    i18n.global.locale.value = locale;
}


export default i18n;