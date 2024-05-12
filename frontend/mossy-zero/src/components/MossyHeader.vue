<script setup lang="ts">
import { NFlex } from 'naive-ui'
import HeaderAction from './common/HeaderAction.vue'
import { useAuthStore } from '@/stores/AuthStore'
import MainMenu from './common/MainMenu.vue'

const authStore = useAuthStore()
</script>

<template>
    <n-flex justify="space-between"
        class="z-40 sticky top-0 font-bold underline bg-opacity-30 backdrop-filter backdrop-blur-md shadow-lg h-12 flex items-center justify-center">
        <p>MOSSY</p>
        <div style="width: 300px;" class="hidden sm:block">我是搜索框</div>
        <HeaderAction />
    </n-flex>
</template>
