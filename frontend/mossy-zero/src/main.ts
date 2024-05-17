import { createApp } from 'vue'
import App from './App.vue'
import i18n, { setI18nLanguage } from './i18n'
import router from './router'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import VMdPreview from '@kangc/v-md-editor/lib/preview'
import '@kangc/v-md-editor/lib/style/preview.css'
import vuePressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js'
import '@kangc/v-md-editor/lib/theme/style/github.css'
import '@/assets/main.css'
import 'notyf/notyf.min.css'
import hljs from 'highlight.js'


async function init() {
    await setI18nLanguage('zh-CN')
    const app = createApp(App)
    const pinia = createPinia()
    pinia.use(piniaPluginPersistedstate)
    app.use(i18n)
    app.use(router)
    app.use(pinia)
    VMdPreview.use(vuePressTheme, {
        Hljs: hljs,
    })
    app.use(VMdPreview)
    app.mount('#app')
}

init()