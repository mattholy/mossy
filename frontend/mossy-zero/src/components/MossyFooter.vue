<script setup lang="ts">
    import { h, ref, onMounted, watch, computed, reactive } from 'vue'
    import type { Component } from 'vue'
    import { NFlex, NButton, NInput, NIcon, NIconWrapper } from 'naive-ui'
    import { useAuthStore } from '@/stores/authStore'
    import { useThemeStore } from '@/stores/themeStore'
    import { useI18n } from 'vue-i18n'
    import { useRoute } from 'vue-router'
    import {
        Home, HomeOutline,
        Compass, CompassOutline,
        Notifications, NotificationsOutline,
        Mail, MailOutline,
        Bookmark, BookmarkOutline,
        Cog, CogOutline,
        Add as AddIcon
    } from '@vicons/ionicons5'

    const authStore = useAuthStore()
    const selectedValue = ref('')
    const theme = useThemeStore()
    const { t } = useI18n()
    const route = useRoute()
    const classMy = computed(() => {
        return theme.isDarkMode ? "backdrop-brightness-50" : ""
    })
    onMounted(() => {
        watch(() => route.path, () => {
            selectedValue.value = window.location.hash.split('/')[1] || '';
        });
    })
</script>

<template>
    <n-flex justify="space-around" :class="classMy"
        class="flex z-40 sticky bottom-0 bg-opacity-30 backdrop-blur-lg h-14 items-center justify-center border-gray-500 border-solid border-t border-b-0 border-l-0 border-r-0 box-border">
        <n-icon :size="24">
            <Home v-if="selectedValue == 'home'" />
            <HomeOutline />
        </n-icon>
        <n-icon :size="24">
            <!-- <Compass /> -->
            <CompassOutline />
        </n-icon>
        <n-button v-if="authStore.isLoggedIn" circle size="large" type="primary">
            <template #icon>
                <AddIcon />
            </template>
        </n-button>
        <n-icon :size="24">
            <!-- <Mail /> -->
            <MailOutline />
        </n-icon>
        <n-icon :size="24">
            <!-- <Bookmark /> -->
            <BookmarkOutline />
        </n-icon>
    </n-flex>
</template>

<style scoped></style>
