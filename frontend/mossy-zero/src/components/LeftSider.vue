<script setup lang="ts">
    import { RouterView } from 'vue-router'
    import { NFlex, NDivider } from 'naive-ui';
    import AuthSection from '@/components/support/AuthSection.vue'
    import Navigator from '@/components/support/NavigationSection.vue'
    import { useUserStateStore } from '@/stores/userStateStore'

    const userStateStore = useUserStateStore()
</script>

<template>
    <n-flex vertical class="">
        <div style="border-bottom: 1px solid grey;">
            <Navigator />
        </div>
        <div style="border-bottom: 1px solid grey;" class="p-2" v-if="!userStateStore.isLoggedIn">
            <AuthSection />
        </div>
    </n-flex>
</template>