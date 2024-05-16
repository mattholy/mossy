<script setup lang="ts">
    import { NSpace } from 'naive-ui';
    import Theme from './ThemeBtn.vue'
    import LocalizationBtn from './LocalizationBtn.vue';
    import ToolKit from './ToolKitBtn.vue'
</script>

<template>
    <div class="hidden md:block">
        <n-space size="small">
            <Theme />
            <LocalizationBtn />
        </n-space>
    </div>
    <div class="md:hidden">
        <n-space size="small">
            <ToolKit />
        </n-space>
    </div>
</template>
