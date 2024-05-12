<script setup lang="ts">
import { computed, watchEffect, onMounted, onUnmounted, ref, reactive } from 'vue'
import { RouterView } from 'vue-router'
import setupSever from '@/setupServer.vue'
import ErrorView from '@/components/ErrorPage.vue'
import MossyHeader from '@/components/MossyHeader.vue'
import LeftSider from '@/components/LeftSider.vue'
import RightSider from '@/components/RightSider.vue'
import { NScrollbar, NMessageProvider, NFlex, NGrid, NGridItem } from 'naive-ui';
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/stores/ThemeStore'
import { useAuthStore } from '@/stores/AuthStore'
import { useI18n } from 'vue-i18n'
import { darkTheme, useOsTheme, useThemeVars, NConfigProvider, NGlobalStyle } from 'naive-ui'
import { MossySetupService } from '@/client/services.gen'
import { $ApiServiceSetupStatus } from '@/client/schemas.gen'
import { OpenAPI } from '@/client/core/OpenAPI'
import { notyf } from '@/utils/notyf'
import { browserSupportsWebAuthn } from '@simplewebauthn/browser'


const authStore = useAuthStore()
const router = useRouter()
const { t } = useI18n()
const themeStore = useThemeStore()
const osThemeRef = useOsTheme()
const theme = computed(() => themeStore.isDarkMode ? darkTheme : null)
const themeVars = useThemeVars()
const showSetupPage = ref(false)
const showRouterPage = ref(false)
const showErrorPage = ref(false)
const errorPageMsg = ref('UnkownError')

watchEffect(() => {
  themeStore.setDarkMode(osThemeRef.value === 'dark');
});

onMounted(async () => {
  OpenAPI.BASE = import.meta.env.VITE_BASE_URL || ''
  await checkStatus()
})

const checkStatus = async () => {
  if (browserSupportsWebAuthn()) {
    showErrorPage.value = false
  } else {
    showErrorPage.value = true
    errorPageMsg.value = 'CoreAPINotReady'
    return false
  }
  await MossySetupService.setupStatusSetupStatusPost()
    .then(
      (res) => {
        if (res.payload.status === 'AllDone') {
          showRouterPage.value = true
        } else {
          showSetupPage.value = true
        }
      }
    )
    .catch(
      (err) => {
        showErrorPage.value = true
        errorPageMsg.value = err.message
      }
    )
  return true
}
</script>

<template>
  <div class="h-dvh">
    <n-config-provider :theme="theme">
      <n-global-style />
      <NScrollbar trigger="hover" content-class="h-dvh">
        <n-message-provider>
          <MossyHeader />
          <setupSever v-if="showSetupPage" />
          <n-flex v-else-if="showRouterPage" justify="center" class="flex absolute top-0 w-full h-dvh">
            <div class="flex-none h-dvh w-1/5 md:w-64 xl:w-72">
              <NScrollbar trigger="hover" content-class="pt-12">
                <LeftSider />
              </NScrollbar>
            </div>
            <div class="grow h-dvh max-w-6xl w-2/5 border border-solid">
              <NScrollbar trigger="hover" content-class="pt-12 ">
                <RouterView />
              </NScrollbar>
            </div>
            <div class="flex-none h-dvh w-1/5 md:w-64 xl:w-72">
              <NScrollbar trigger="hover" content-class="pt-12">
                <RightSider />
              </NScrollbar>
            </div>
          </n-flex>

          <ErrorView v-else-if="showErrorPage" :msg="errorPageMsg" />
        </n-message-provider>
      </NScrollbar>
    </n-config-provider>
  </div>
</template>

<style scoped></style>
