<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { NButton, NFlex, NIcon, NModal } from 'naive-ui'
import { FingerPrint } from '@vicons/ionicons5'
import { webauthnAuthentication } from '@/utils/webauthn'
import { notyf } from '@/utils/notyf'
import { useAuthStore } from '@/stores/AuthStore'

const showReg = ref(false)
const { t } = useI18n()
const authStore = useAuthStore()
const login = async () => {
    await webauthnAuthentication()
        .then((res) => {
            authStore.setToken(res)
        })
        .catch((err) => {
            notyf.error(t(`api.statusmsg.${err.message}.notification`))
        })

}
</script>

<template>
    <n-flex vertical class="fade-in-up">
        <p class="px-2">
            {{ t('ui.leftsider.loginandreg.desc') }}
        </p>
        <p class="px-2 py-2 font-bold ">
            {{ t('ui.leftsider.loginandreg.saftyfirst') }}
        </p>
        <n-button round size="large" type="primary" @click="showReg = true">
            {{ t('ui.common_desc.register') }}
        </n-button>
        <n-button round size="large" strong ghost type="primary" @click="login">
            <template #icon>
                <n-icon>
                    <FingerPrint />
                </n-icon>
            </template>
            {{ t('ui.common_desc.login') }}
        </n-button>


        <n-modal v-model:show="showReg" preset="card" title="创建账户" size="huge" :bordered="true">
            内容
            <template #footer>
                尾部
            </template>
        </n-modal>
    </n-flex>
</template>