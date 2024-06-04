<script setup lang="ts">
    import { RouterView } from 'vue-router'
    import { NFlex } from 'naive-ui';
    import UserProfileCard from './common/UserProfileCard.vue';
    import NormalStatusEditor from './common/NormalStatusEditor.vue';
</script>

<template>
    <n-flex vertical>
        <UserProfileCard />
        <NormalStatusEditor />

    </n-flex>
</template>