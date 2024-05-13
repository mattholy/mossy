<script setup lang="ts">
import { RouterView } from 'vue-router'
import { NFlex, NDivider } from 'naive-ui';
import AuthSection from '@/components/support/AuthSection.vue'
import Navigator from '@/components/support/NavigationSection.vue'
import { useAuthStore } from '@/stores/AuthStore'

const authStore = useAuthStore()
</script>

<template>
    <n-flex vertical class="py-4 pt-8">
        <Navigator />
        <n-divider v-if="!authStore.isLoggedIn" />
        <AuthSection v-if="!authStore.isLoggedIn" />
    </n-flex>
</template>