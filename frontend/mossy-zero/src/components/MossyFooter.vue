<script setup lang="ts">
    import { ref, computed } from 'vue'
    import { NFlex, NInput, NIcon } from 'naive-ui'
    import HeaderAction from './common/HeaderAction.vue'
    import { useAuthStore } from '@/stores/authStore'
    import { useThemeStore } from '@/stores/themeStore'
    import MainMenu from './common/MainMenu.vue'
    import { Search, FlashOutline } from '@vicons/ionicons5'
    import { useI18n } from 'vue-i18n'

    const authStore = useAuthStore()
    const theme = useThemeStore()
    const { t } = useI18n()
    const classMy = computed(() => {
        return theme.isDarkMode ? "backdrop-brightness-50" : ""
    })
</script>

<template>
    <n-flex justify="space-between" :class="classMy"
        class="flex z-40 sticky bottom-0 bg-opacity-30 backdrop-blur-lg h-12  items-center justify-center border-gray-400 border-solid border-t-0 border-b-0 md:border-b border-l-0 border-r-0">
        <div class="w-1/5 h-full flex items-center justify-start">
            MOSSY
        </div>
        <div class="hidden md:flex items-center justify-center w-96">
            <n-input clearable round :placeholder="t('ui.common_desc.search')">
                <template #prefix>
                    <n-icon>
                        <Search />
                    </n-icon>
                </template>
            </n-input>
        </div>
        <div class="w-1/5 h-full flex items-center justify-end">
            <HeaderAction />
        </div>
    </n-flex>
</template>

<style scoped>
    input {
        backdrop-filter: blur(10px);
        background-color: rgba(187, 187, 187, .5);
        color: black !important;
    }
</style>
