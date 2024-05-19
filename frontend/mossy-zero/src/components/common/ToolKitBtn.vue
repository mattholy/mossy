<script setup lang="ts">
    import { ref } from 'vue'
    import { NTag, NDropdown, NSpace, NButton, NIcon, NDrawer, NDrawerContent, NFlex, NSwitch, NDivider } from "naive-ui"
    import { Menu as MenuIcon, ChevronForward } from "@vicons/ionicons5"
    import { useI18n } from 'vue-i18n'
    import { useThemeStore } from '@/stores/themeStore'
    import { useLocalizationStore } from '@/stores/localizationStore'
    import { useRouter } from 'vue-router'

    const localizationStore = useLocalizationStore()
    const { t } = useI18n()
    const themeStore = useThemeStore()
    const router = useRouter()
    const active = ref(false)
    const activate = () => {
        active.value = true
    }
    const handleChangeLang = (key: string) => {
        localizationStore.setLanguage(key)
    }
    const optionsLangs = [
        {
            label: '中文',
            key: 'zh-CN'
        },
        {
            label: 'English',
            key: "en-US"
        }
    ] 
</script>

<template>
    <n-button ghost :bordered=false :focusable=false @click="activate" size="large" type="primary" class="h-12">
        <n-icon>
            <MenuIcon />
        </n-icon>
    </n-button>
    <n-drawer v-model:show="active" :max-width=400 placement="right">
        <n-drawer-content>
            <template #header>
                {{ t('ui.header.actions.more') }}
            </template>
            <n-space vertical size="large">
                <n-flex justify="space-between" class="leading-8 h-8 items-center">
                    <span>{{ t('ui.header.actions.darkmode') }}</span>
                    <n-switch v-model:value="themeStore.isDarkMode" />
                </n-flex>
                <n-flex justify="space-between" class="leading-8 h-8 items-center">
                    <span>{{ t('ui.header.actions.localization') }}</span>
                    <n-dropdown trigger="hover" :options="optionsLangs" @select="handleChangeLang" size="huge"
                        :show-arrow="true">
                        <n-tag>{{ localizationStore.currentLanguage }}</n-tag>
                    </n-dropdown>
                </n-flex>
                <n-divider />
                <n-flex justify="space-between" class="leading-8 h-8 items-center cursor-pointer"
                    @click="active = false; router.push('/')">
                    <span>{{ t('ui.header.actions.notification') }}</span>
                    <n-icon>
                        <ChevronForward />
                    </n-icon>
                </n-flex>
            </n-space>
            <template #footer>
                <n-flex class="w-full" justify="space-evenly">
                    <n-button secondary type="primary" @click="active = false; router.push('/settings')">{{
                        t('ui.header.actions.settings')
                        }}</n-button>
                    <n-button secondary type="error">{{ t('ui.header.actions.logout') }}</n-button>

                </n-flex>
            </template>
        </n-drawer-content>
    </n-drawer>
</template>

<style scoped></style>