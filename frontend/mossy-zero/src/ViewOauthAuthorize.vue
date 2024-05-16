<script setup lang="ts">
    import { useRouter, useRoute } from 'vue-router'
    import { callMossyApi, MossyApiError } from './utils/apiCall'
    import { useThemeStore } from '@/stores/themeStore'
    import { useAuthStore } from '@/stores/authStore'
    import { useI18n } from 'vue-i18n'

    const authStore = useAuthStore()
    const route = useRoute()
    const router = useRouter()
</script>

<template>
    {{ route.query.client_id }}
</template>