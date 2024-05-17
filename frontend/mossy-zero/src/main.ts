// main.ts
import { createApp } from 'vue';
import App from './App.vue';
import i18n, { setI18nLanguage } from './i18n';
import router from './router';
import myPinia from '@/pinia';
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import vuePressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import '@/assets/main.css';
import 'notyf/notyf.min.css';
import hljs from 'highlight.js';

const app = createApp(App);

app.use(i18n);
app.use(router);
app.use(myPinia);
VMdPreview.use(vuePressTheme, {
    Hljs: hljs,
});
app.use(VMdPreview);

async function init() {
    await setI18nLanguage('zh-CN');
    app.mount('#app');
}

init();
