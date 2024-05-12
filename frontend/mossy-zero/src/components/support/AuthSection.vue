<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { NButton, NFlex, NIcon, NModal } from 'naive-ui'
import { FingerPrint } from '@vicons/ionicons5'
import { webauthnAuthentication } from '@/utils/webauthn'
import { notyf } from '@/utils/notyf'

const showReg = ref(false)
const { t } = useI18n()
const login = async () => {
    const token = await webauthnAuthentication()
        .catch((err) => {
            notyf.error(t(`api.statusmsg.${err.message}.notification`))
        })
}
</script>

<template>
    <n-flex vertical>
        <p class="px-2">
            {{ t('ui.leftsider.loginandreg.desc') }}
        </p>
        <p class="px-2 py-2 font-bold ">Mossy不会记录你的任何个人信息，注册只需要提供用户名。</p>
        <n-button round size="large" type="primary" @click="showReg = true">
            创建账户
        </n-button>
        <n-button round size="large" strong ghost type="primary" @click="login">
            <template #icon>
                <n-icon>
                    <FingerPrint />
                </n-icon>
            </template>
            登录
        </n-button>


        <n-modal v-model:show="showReg" preset="card" title="创建账户" size="huge" :bordered="true">
            内容
            <template #footer>
                尾部
            </template>
        </n-modal>
    </n-flex>
</template>