<script setup lang="ts">
    import { h, ref, onMounted, watch, computed, reactive } from 'vue'
    import type { Component } from 'vue'
    import { NFlex, NButton, NInput, NIcon, NIconWrapper } from 'naive-ui'
    import { useUserStateStore } from '@/stores/userStateStore'
    import { useThemeStore } from '@/stores/themeStore'
    import { useI18n } from 'vue-i18n'
    import { useRoute, useRouter } from 'vue-router'
    import {
        Home, HomeOutline,
        Compass, CompassOutline,
        Notifications, NotificationsOutline,
        Mail, MailOutline,
        Bookmark, BookmarkOutline,
        Cog, CogOutline,
        InformationCircle, InformationCircleOutline,
        Add as AddIcon
    } from '@vicons/ionicons5'

    const userStateStore = useUserStateStore()
    const selectedValue = ref(window.location.hash.split('/')[1] || '')
    const theme = useThemeStore()
    const { t } = useI18n()
    const route = useRoute()
    const router = useRouter()
    const bgcolor = computed(() => {
        return theme.isDarkMode ? "bg-neutral-700/70" : "bg-neutral-50/70"
    })
    onMounted(() => {
        watch(() => route.path, () => {
            selectedValue.value = window.location.hash.split('/')[1] || '';
            console.log(selectedValue.value)
        });
    })
</script>

<template>
    <n-flex justify="space-around"
        class="flex z-40 sticky bottom-0 backdrop-blur-lg h-14 items-center justify-center border-gray-500 border-solid border-t border-b-0 border-l-0 border-r-0"
        :class="bgcolor">
        <div class="h-14 px-4 flex items-center justify-center" v-if="userStateStore.isLoggedIn"
            @click="router.push('home')">
            <n-icon :size="32">
                <Home v-if="selectedValue == 'home'" />
                <HomeOutline v-else />
            </n-icon>
        </div>
        <div class="h-14 px-4 flex items-center justify-center" @click="router.push('explore')">
            <n-icon :size="32">
                <Compass v-if="selectedValue == 'explore'" />
                <CompassOutline v-else />
            </n-icon>
        </div>
        <n-button v-if="userStateStore.isLoggedIn" circle size="large" type="primary">
            <template #icon>
                <AddIcon />
            </template>
        </n-button>
        <div class="h-14 px-4 flex items-center justify-center" v-if="userStateStore.isLoggedIn"
            @click="router.push('conversations')">
            <n-icon :size="32">
                <Mail v-if="selectedValue == 'conversations'" />
                <MailOutline v-else />
            </n-icon>
        </div>
        <div class="h-14 px-4 flex items-center justify-center" v-if="userStateStore.isLoggedIn"
            @click="router.push('collections')">
            <n-icon :size="32">
                <Bookmark v-if="selectedValue == 'collections'" />
                <BookmarkOutline v-else />
            </n-icon>
        </div>
        <div class="h-14 px-4 flex flex-col gap-0 items-center justify-center" v-if="!userStateStore.isLoggedIn"
            @click="router.push('about')">
            <n-icon :size="32">
                <InformationCircle v-if="selectedValue == 'about'" />
                <InformationCircleOutline v-else />
            </n-icon>
            <!-- <span>关于</span> -->
        </div>
    </n-flex>
</template>

<style scoped></style>
