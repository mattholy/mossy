<script setup lang="ts">
    import { NFlex, NButton, NIcon } from 'naive-ui'
    import { useRoute, useRouter } from 'vue-router'
    import { ChevronBack, ShareSocial } from '@vicons/ionicons5'
    import { useI18n } from 'vue-i18n'
    import SubpageHeader from '@/components/support/SubpageHeader.vue'

    const route = useRoute()
    const router = useRouter()
    const { t } = useI18n()
    const username = route.params.id
</script>

<template>
    <SubpageHeader pageCategory="user" :resourceUri="route.params.id as string" />
</template>