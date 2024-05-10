<script setup lang="ts">
import { NFlex } from 'naive-ui'
import HeaderAction from './common/HeaderAction.vue'
</script>

<template>
    <n-flex justify="space-between"
        class="z-40 sticky top-0 font-bold underline bg-opacity-30 backdrop-filter backdrop-blur-md shadow-lg h-12 flex items-center justify-center">
        <p>MOSSY</p>
        <HeaderAction />
    </n-flex>
</template>
