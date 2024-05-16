<script setup lang="ts">
    import { h, ref, onMounted, watch, computed, reactive } from 'vue'
    import type { Component } from 'vue'
    import { useI18n } from 'vue-i18n'
    import { NMenu, NIcon } from 'naive-ui'
    import type { MenuOption } from 'naive-ui'
    import { RouterLink } from 'vue-router'
    import {
        Home, HomeOutline,
        Compass, CompassOutline,
        Notifications, NotificationsOutline,
        Mail, MailOutline,
        Bookmark, BookmarkOutline,
        Cog, CogOutline
    } from '@vicons/ionicons5'
    import { useRoute } from 'vue-router'
    import { useAuthStore } from '@/stores/authStore'

    const { t } = useI18n()
    const route = useRoute()
    const authStore = useAuthStore()
    const isLoggedIn = computed(() => authStore.isLoggedIn);
    function renderIcon(key: string, icon: Component, iconSeleted: Component) {
        return () => h(NIcon, null, { default: () => h(key == selectedValue.value ? icon : iconSeleted) })
    }

    const menuOptions = computed(() => [
        {
            label: () =>
                h(
                    RouterLink,
                    {
                        to: {
                            path: '/home'
                        },
                        class: 'text-xl'
                    },
                    { default: () => t('ui.leftsider.navigater.home') }
                ),
            key: 'home',
            icon: renderIcon('home', Home, HomeOutline),
            show: isLoggedIn.value
        },
        {
            label: () =>
                h(
                    RouterLink,
                    {
                        to: {
                            path: '/explore'
                        },
                        class: 'text-xl'
                    },
                    { default: () => t('ui.leftsider.navigater.explore') }
                ),
            key: 'explore',
            icon: renderIcon('explore', Compass, CompassOutline),
            show: true
        },
        {
            label: () =>
                h(
                    RouterLink,
                    {
                        to: {
                            path: '/notifications'
                        },
                        class: 'text-xl'
                    },
                    { default: () => t('ui.leftsider.navigater.notifications') }
                ),
            key: 'notifications',
            icon: renderIcon('notifications', Notifications, NotificationsOutline),
            show: isLoggedIn.value
        },
        {
            label: () =>
                h(
                    RouterLink,
                    {
                        to: {
                            path: '/conversations'
                        },
                        class: 'text-xl'
                    },
                    { default: () => t('ui.leftsider.navigater.conversations') }
                ),
            key: 'conversations',
            icon: renderIcon('conversations', Mail, MailOutline),
            show: isLoggedIn.value
        },
        {
            label: () =>
                h(
                    RouterLink,
                    {
                        to: {
                            path: '/collections'
                        },
                        class: 'text-xl'
                    },
                    { default: () => t('ui.leftsider.navigater.collections') }
                ),
            key: 'collections',
            icon: renderIcon('collections', Bookmark, BookmarkOutline),
            show: isLoggedIn.value
        },
        {
            label: () =>
                h(
                    RouterLink,
                    {
                        to: {
                            path: '/settings'
                        },
                        class: 'text-xl'
                    },
                    { default: () => t('ui.leftsider.navigater.settings') }
                ),
            key: 'settings',
            icon: renderIcon('settings', Cog, CogOutline),
            show: authStore.isLoggedIn
        },
    ])
    const selectedValue = ref<string>(window.location.hash.split('/')[1] || '');

    onMounted(() => {
        watch(() => route.path, () => {
            selectedValue.value = window.location.hash.split('/')[1] || '';
        });
    })
</script>

<template>
    <n-menu :icon-size="25" v-model:value="selectedValue" accordion :options="menuOptions"
        @click="console.log(selectedValue)" class="transition duration-300 ease-in-out" />

</template>

<style scoped></style>