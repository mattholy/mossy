<script setup lang="ts">
import { computed, watchEffect, onMounted, onUnmounted, ref, reactive } from 'vue'
import { RouterView } from 'vue-router'
import setupSever from '@/setupServer.vue'
import ErrorView from '@/components/ErrorPage.vue'
import MossyHeader from '@/components/MossyHeader.vue'
import LeftSider from '@/components/LeftSider.vue'
import RightSider from '@/components/RightSider.vue'
import { NScrollbar, NMessageProvider, NFlex, NCard, NAlert } from 'naive-ui';
import { useRouter, useRoute } from 'vue-router'
import { useThemeStore } from '@/stores/ThemeStore'
import { useAuthStore } from '@/stores/AuthStore'
import { useI18n } from 'vue-i18n'
import { darkTheme, useOsTheme, useThemeVars, NConfigProvider, NGlobalStyle } from 'naive-ui'
import { MossySetupService } from '@/client/services.gen'
import { $ApiServiceSetupStatus } from '@/client/schemas.gen'
import { OpenAPI } from '@/client/core/OpenAPI'
import { notyf } from '@/utils/notyf'
import { browserSupportsWebAuthn } from '@simplewebauthn/browser'
import { callMossyApi, MossyApiError } from './utils/apiCall'


const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const { t } = useI18n()
const themeStore = useThemeStore()
const osThemeRef = useOsTheme()
const theme = computed(() => themeStore.isDarkMode ? darkTheme : null)
const themeVars = useThemeVars()
const showSetupPage = ref(false)
const showRouterPage = ref(false)
const showErrorPage = ref(false)
const errorPageMsg = ref('UnkownError')
const showOauthPage = ref(false)

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
  }

  await callMossyApi({
    endpoint: '/setup/status'
  })
    .then((res) => {
      if (res.status === 'AllDone') {
        // TODO: check oauth status
        if (route.query.test == 'oauth') {
          showOauthPage.value = true
        } else {
          showRouterPage.value = true
          showSetupPage.value = false
          showErrorPage.value = false
        }
      } else {
        showRouterPage.value = false
        showSetupPage.value = true
        showErrorPage.value = false
      }
    })
    .catch((error) => {
      if (error instanceof MossyApiError) {
        showErrorPage.value = true
        errorPageMsg.value = error.detail
      } else {
        showErrorPage.value = true
        errorPageMsg.value = 'UnkownError'
      }
    })
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
          <n-flex v-else-if="showRouterPage" justify="center" class="flex absolute top-0 w-full h-dvh" style="gap: 0;">
            <div
              class="hidden md:flex 2xl:border-l flex-none h-dvh w-1/5 md:w-64 xl:w-72 m-0 p-0 border-gray-400 border-solid border-0">
              <NScrollbar trigger="hover" content-class="pt-12">
                <LeftSider />
              </NScrollbar>
            </div>
            <div
              class="grow h-dvh max-w-5xl w-2/5 m-0 p-0 z-30 lg:border-r md:border-l border-gray-400 border-solid border-0">
              <NScrollbar trigger="hover" content-class="pt-12 border-x-2 border-slate-800">
                <RouterView />
              </NScrollbar>
            </div>
            <div
              class="hidden lg:flex 2xl:border-r flex-none h-dvh w-1/5 md:w-64 xl:w-72 m-0 p-0 border-gray-400 border-solid border-0">
              <NScrollbar trigger="hover" content-class="pt-12">
                <RightSider />
              </NScrollbar>
            </div>
          </n-flex>
          <ErrorView v-else-if="showErrorPage" :msg="errorPageMsg" />
          <div v-else-if="showOauthPage"> {{ route.query.test }}</div>
        </n-message-provider>
      </NScrollbar>
    </n-config-provider>
  </div>
</template>

<style>
.n-modal-mask {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  backdrop-filter: blur(5px);
}

.n-drawer-mask {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  backdrop-filter: blur(5px);
}
</style>
