<script setup lang="ts">
import { ref } from 'vue'
import { NButton, NIcon, NDrawer, NDrawerContent, NFlex } from "naive-ui"
import { Menu } from "@vicons/ionicons5"
import { useI18n } from 'vue-i18n'
import { useThemeStore } from '@/stores/ThemeStore'

const { t } = useI18n()
const themeStore = useThemeStore()

const active = ref(false)
const activate = () => {
    active.value = true
}
</script>

<template>
    <n-button circle ghost :bordered=false :focusable=false @click="activate">
        <n-icon>
            <Menu />
        </n-icon>
    </n-button>
    <n-drawer v-model:show="active" :max-width=400 placement="right">
        <n-drawer-content>
            <template #header>
                {{ t('ui.header.actions.more') }}
            </template>
            <n-flex vertical>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
                <n-button>ToolKit</n-button>
            </n-flex>
            <template #footer>
                <n-button>Footer</n-button>
            </template>
        </n-drawer-content>
    </n-drawer>
</template>

<style scoped></style>