<script setup lang="ts">
    import { NTooltip, NButton, NIcon } from "naive-ui"
    import { SunnyOutline } from "@vicons/ionicons5"
    import { useI18n } from 'vue-i18n'
    import { useThemeStore } from '@/stores/themeStore'

    const { t } = useI18n()
    const themeStore = useThemeStore()
</script>

<template>
    <n-tooltip trigger="hover">
        <template #trigger>
            <n-button circle strong ghost @click="themeStore.toggleDarkMode()">
                <n-icon>
                    <SunnyOutline />
                </n-icon>
            </n-button>
        </template>
        {{ t('ui.header.actions.darkmode') }}
    </n-tooltip>
</template>

<style scoped></style>