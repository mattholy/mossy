<script setup lang="ts">
import { NSpace } from 'naive-ui';
import Theme from './ThemeBtn.vue'
import LocalizationBtn from './LocalizationBtn.vue';
</script>

<template>
    <div class="px-2">
        <n-space size="small">
            <Theme />
            <LocalizationBtn />
        </n-space>
    </div>
</template>
