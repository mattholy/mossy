<script setup lang="ts">
import { RouterView } from 'vue-router'
import { NFlex, NDivider } from 'naive-ui';
import AuthSection from '@/components/support/AuthSection.vue'
</script>

<template>
    <n-flex vertical class="p-4">
        <n-divider />
        <AuthSection />
        <n-divider />
    </n-flex>
</template>