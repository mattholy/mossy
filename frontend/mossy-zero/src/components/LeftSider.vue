<script setup lang="ts">
    import { RouterView } from 'vue-router'
    import { NFlex, NDivider } from 'naive-ui';
    import AuthSection from '@/components/support/AuthSection.vue'
    import Navigator from '@/components/support/NavigationSection.vue'
    import { useUserStateStore } from '@/stores/userStateStore'
    import { useI18n } from 'vue-i18n';

    const userStateStore = useUserStateStore()
    const version = import.meta.env.VITE_MOSSY_VERSION
    const env = import.meta.env.VITE_ENV
    const { t } = useI18n()
</script>

<template>
    <n-flex vertical class="">
        <div class="border-b border-gray-500 border-solid border-0">
            <Navigator />
        </div>
        <div class="border-b border-gray-500 border-solid border-0 p-2" v-if="!userStateStore.isLoggedIn">
            <AuthSection />
        </div>
    </n-flex>
    <div class="border-b border-gray-500 border-solid border-0 text-center font-light">
        <p class="p-0 m-0">Mossy - {{ env ? "Dev" : "Pro" }} - {{ version }}</p>
        <p class="p-0 m-0">
            <a>{{ t('ui.leftsider.footer.about') }}</a>
            ·
            <a>{{ t('ui.leftsider.footer.sourcecode') }}</a>
        </p>
    </div>
</template>