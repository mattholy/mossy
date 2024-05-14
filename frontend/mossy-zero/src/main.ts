import { createApp } from 'vue'
import App from './App.vue'
import i18n, { setI18nLanguage } from './i18n'
import router from './router'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { VueShowdownPlugin } from 'vue-showdown'
import '@/assets/main.css'
import 'notyf/notyf.min.css'

async function init() {
    await setI18nLanguage('zh-CN')
    const app = createApp(App)
    const pinia = createPinia()
    pinia.use(piniaPluginPersistedstate)
    app.use(i18n)
    app.use(router)
    app.use(pinia)
    app.use(VueShowdownPlugin, {
        flavor: 'github'
    })
    app.mount('#app')
}

init()