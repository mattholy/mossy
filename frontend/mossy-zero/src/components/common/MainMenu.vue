<script setup lang="ts">
    import { ref } from 'vue'
    import { NButton, NIcon, NDrawer, NDrawerContent } from "naive-ui"
    import { Menu } from "@vicons/ionicons5"
    import { useI18n } from 'vue-i18n'
    import { useThemeStore } from '@/stores/themeStore'

    const { t } = useI18n()
    const themeStore = useThemeStore()

    const active = ref(false)
    const activate = () => {
        active.value = true
    }
</script>

<template>
    <n-button circle secondary ghost @click="activate">
        <n-icon>
            <Menu />
        </n-icon>
    </n-button>
    <n-drawer v-model:show="active" :max-width=400 placement="left">
        <n-drawer-content body-style="background-color:red" title='123'>
            2323
        </n-drawer-content>
    </n-drawer>
</template>

<style scoped></style>