<script setup lang="ts">
    import { ref, computed } from 'vue'
    import { NFlex, NInput, NIcon } from 'naive-ui'
    import HeaderAction from './common/HeaderAction.vue'
    import { useUserStateStore } from '@/stores/userStateStore'
    import { useThemeStore } from '@/stores/themeStore'
    import MainMenu from './common/MainMenu.vue'
    import { Search, FlashOutline } from '@vicons/ionicons5'
    import { useI18n } from 'vue-i18n'
    import AuthSection from '@/components/support/AuthSection.vue'
    import { useWindowSize } from '@vueuse/core'

    const { width } = useWindowSize()
    const small_device = computed(() => width.value < 768)
    const userStateStore = useUserStateStore()
    const theme = useThemeStore()
    const { t } = useI18n()
    const bgcolor = computed(() => {
        return theme.isDarkMode ? "bg-neutral-700/70" : "bg-neutral-50/70"
    })
</script>

<template>
    <n-flex justify="space-between"
        class="z-40 sticky top-0 backdrop-blur-lg h-12 flex items-center justify-center border-gray-500 border-solid border-t-0 border-b border-l-0 border-r-0 box-border"
        :class="bgcolor">
        <div class="h-full flex items-center justify-start">
            <AuthSection v-if="small_device && !userStateStore.isLoggedIn" />
            <p v-else>Mossy Logo</p>
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
        <div class="h-full flex items-center justify-end">
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
