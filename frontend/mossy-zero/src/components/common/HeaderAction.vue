<script setup lang="ts">
import { NSpace } from 'naive-ui';
import Theme from './ThemeBtn.vue'
import LocalizationBtn from './LocalizationBtn.vue';
import ToolKit from './ToolKitBtn.vue'
</script>

<template>
    <div class="px-2 hidden sm:block">
        <n-space size="small">
            <Theme />
            <LocalizationBtn />
        </n-space>
    </div>
    <div class="px-2 sm:hidden">
        <n-space size="small">
            <ToolKit />
            <!-- <Theme />
            <LocalizationBtn /> -->
        </n-space>
    </div>
</template>
