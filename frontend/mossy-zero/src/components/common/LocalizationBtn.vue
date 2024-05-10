<script setup lang="ts">
import { NTooltip, NButton, NIcon, NDropdown } from "naive-ui"
import { LanguageOutline } from "@vicons/ionicons5"
import { setI18nLanguage } from '@/i18n'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const langs = [
    {
        label: '🇨🇳 中文',
        key: 'zh-CN'
    },
    {
        label: '🇺🇸 English',
        key: "en-US"
    }
]

function handleSelect(key: string | number) {
    setI18nLanguage(String(key))
}

</script>

<template>
    <n-dropdown trigger="click" :options="langs" :show-arrow="true" @select="handleSelect">
        <n-tooltip trigger="hover">
            <template #trigger>
                <n-button circle strong ghost>
                    <n-icon>
                        <LanguageOutline />
                    </n-icon>
                </n-button>
            </template>
            {{ t('ui.header.actions.localization') }}
        </n-tooltip>
    </n-dropdown>
</template>