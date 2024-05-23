<script setup lang="ts">
  import { computed, watchEffect, onMounted, onUnmounted, ref, reactive } from 'vue'
  import { RouterView } from 'vue-router'
  import setupSever from '@/ViewSetupServer.vue'
  import OathPage from '@/ViewOauthAuthorize.vue'
  import ErrorView from '@/components/ErrorPage.vue'
  import MossyHeader from '@/components/MossyHeader.vue'
  import MossyFooter from '@/components/MossyFooter.vue'
  import LeftSider from '@/components/LeftSider.vue'
  import RightSider from '@/components/RightSider.vue'
  import { NScrollbar, NMessageProvider, NFlex, NCard, NAlert, NDialogProvider, NLoadingBarProvider } from 'naive-ui';
  import type { GlobalThemeOverrides } from 'naive-ui'
  import { useRouter, useRoute } from 'vue-router'
  import { useThemeStore } from '@/stores/themeStore'
  import { useUserStateStore } from '@/stores/userStateStore'
  import { useLocalizationStore } from '@/stores/localizationStore'
  import { useI18n } from 'vue-i18n'
  import { darkTheme, useOsTheme, useThemeVars, NConfigProvider, NGlobalStyle } from 'naive-ui'
  import { MossySetupService } from '@/client/services.gen'
  import { $ApiServiceSetupStatus } from '@/client/schemas.gen'
  import { notyf } from '@/utils/notyf'
  import { browserSupportsWebAuthn } from '@simplewebauthn/browser'
  import { callMossyApi, MossyApiError } from './utils/apiCall'
  import { useWindowSize } from '@vueuse/core'


  const userStateStore = useUserStateStore()
  const localizationStore = useLocalizationStore()
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
  const errorPageMsg = ref('UnknownError')
  const showOauthPage = ref(false)
  const { width } = useWindowSize()
  const themeOverrides: GlobalThemeOverrides = {
    "common": {
      "fontFamily": "MiSans"
    }
  }
  const small_device = computed(() => {
    return width.value < 768
  })
  const medium_device = computed(() => {
    return width.value < 1024
  })

  watchEffect(() => {
    themeStore.setDarkMode(osThemeRef.value === 'dark')
  });

  onMounted(async () => {
    await checkStatus()
    localizationStore.setLanguage(navigator.language)
  })

  const checkStatus = async () => {
    if (!browserSupportsWebAuthn()) {
      showErrorPage.value = true
      errorPageMsg.value = 'CoreAPINotReady'
    }

    await callMossyApi({
      endpoint: '/setup/status'
    })
      .then((res) => {
        if (res.status === 'AllDone') {
          if (route.query.authorize && route.query.authorize == 'oauth') {
            showOauthPage.value = true
          } else {
            showRouterPage.value = true
          }
        } else {
          showSetupPage.value = true
        }
      })
      .catch((error) => {
        if (error instanceof MossyApiError) {
          showErrorPage.value = true
          errorPageMsg.value = error.detail
        } else {
          showErrorPage.value = true
          errorPageMsg.value = error.message
        }
      })
  }
</script>

<template>
  <div class="h-dvh">
    <n-config-provider :theme="theme" :locale="localizationStore.currentNaiveUILanguage"
      :date-locale="localizationStore.currentNaiveDateLanguage" :theme-overrides="themeOverrides">
      <n-global-style />
      <n-loading-bar-provider>
        <NScrollbar trigger="hover" class="h-dvh">
          <n-dialog-provider>
            <n-message-provider>
              <MossyHeader />
              <setupSever v-if="showSetupPage" />
              <n-flex v-else-if="showRouterPage" justify="center" class="flex absolute top-0 w-full h-dvh"
                style="gap: 0;">
                <div v-if="!small_device"
                  class="hidden md:flex 2xl:border-l flex-none h-dvh w-1/5 md:w-64 xl:w-72 m-0 p-0 border-gray-500 border-solid border-0">
                  <n-scrollbar trigger="hover" content-class="pt-12">
                    <LeftSider />
                  </n-scrollbar>
                </div>
                <div
                  class="grow h-dvh max-w-5xl w-2/5 m-0 p-0 z-30 lg:border-r md:border-l border-gray-500 border-solid border-0">
                  <NScrollbar trigger="hover" class="h-dvh" content-class="flex flex-col pt-12 min-h-full">
                    <RouterView />
                    <MossyFooter v-if="small_device" class="mt-auto min-h-14 max-h-14" />
                  </NScrollbar>
                </div>
                <div v-if="!medium_device"
                  class="hidden lg:flex 2xl:border-r flex-none h-dvh w-1/5 md:w-64 xl:w-72 m-0 p-0 border-gray-500 border-solid border-0">
                  <NScrollbar trigger="hover" content-class="pt-12">
                    <RightSider />
                  </NScrollbar>
                </div>
              </n-flex>
              <ErrorView v-else-if="showErrorPage" :msg="errorPageMsg" />
              <OathPage v-else-if="showOauthPage" />
            </n-message-provider>
          </n-dialog-provider>
        </NScrollbar>
      </n-loading-bar-provider>
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
