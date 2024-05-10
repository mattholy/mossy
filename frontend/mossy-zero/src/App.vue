<script setup lang="ts">
import { computed, watchEffect, onMounted, onUnmounted } from 'vue'
import { RouterView } from 'vue-router'
import setupSever from '@/setupServer.vue'
import MossyHeader from '@/components/MossyHeader.vue';
import { NScrollbar } from 'naive-ui';
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/ThemeStore'
import { useI18n } from 'vue-i18n'
import { darkTheme, useOsTheme, useThemeVars, NConfigProvider, NGlobalStyle } from 'naive-ui'

const router = useRouter()
const { t } = useI18n()
const themeStore = useThemeStore()
const osThemeRef = useOsTheme()
const theme = computed(() => themeStore.isDarkMode ? darkTheme : null)
const themeVars = useThemeVars()

watchEffect(() => {
  themeStore.setDarkMode(osThemeRef.value === 'dark');
});
</script>

<template>
  <n-config-provider :theme="theme">
    <n-global-style />
    <NScrollbar class="h-screen" trigger="hover">
      <MossyHeader />
      我们在田野上面找猪<br>
      想象中已找到了三只<br>
      小鸟在白云上面追逐<br>
      它们在树底下跳舞<br>
      啦啦啦啦啦啦啦啦咧<br>
      啦啦啦啦咧<br>
      我们在想象中度过了许多年<br>
      想象中我们是如此的疯狂<br>
      我们在城市里面找猪<br>
      想象中已找到了几百万只<br>
      小鸟在公园里面唱歌<br>
      它们独自在想象里跳舞<br>
      啦啦啦啦啦啦啦啦咧<br>
      啦啦啦啦咧<br>
      我们在想象中度过了许多年<br>
      许多年之后我们又开始想象<br>
      啦啦啦啦啦啦啦啦咧
      <setupSever style="height: 1000px;" />
      <RouterView style="height: 1000px;" />
    </NScrollbar>
  </n-config-provider>
</template>

<style scoped></style>
