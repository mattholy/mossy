<script setup lang="ts">
import { ref, computed } from 'vue'
import { NFlex, NInput, NIcon } from 'naive-ui'
import HeaderAction from './common/HeaderAction.vue'
import { useAuthStore } from '@/stores/AuthStore'
import { useThemeStore } from '@/stores/ThemeStore'
import MainMenu from './common/MainMenu.vue'
import { Search, FlashOutline } from '@vicons/ionicons5'
import { useI18n } from 'vue-i18n'

const authStore = useAuthStore()
const theme = useThemeStore()
const { t } = useI18n()
const classMy = computed(() => {
    return theme.isDarkMode ? "border-0 z-40 sticky top-0 bg-opacity-30 backdrop-brightness-50 backdrop-blur-xl h-12 flex items-center justify-center" : "border-0 z-40 sticky top-0 bg-opacity-30 backdrop-brightness-150 backdrop-blur-xl h-12 flex items-center justify-center"
})
</script>

<template>
    <n-flex justify="space-between" :class="classMy" style="border-bottom: 1px solid grey;">
        <p>MOSSY</p>
        <div style="width: 300px;" class="hidden sm:block">
            <n-input clearable round :placeholder="t('ui.common_desc.search')">
                <template #prefix>
                    <n-icon>
                        <Search />
                    </n-icon>
                </template>
            </n-input>
        </div>
        <HeaderAction />
    </n-flex>
</template>

<style scoped>
input {
    backdrop-filter: blur(10px);
    background-color: rgba(187, 187, 187, .5);
    color: black !important;
}
</style>
