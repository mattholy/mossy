<script setup lang="ts">
    import { onBeforeUnmount, ref, computed, watchEffect, h } from 'vue'
    import { useI18n } from 'vue-i18n'
    import { useMessage } from 'naive-ui'
    import { NButton, NFlex, NIcon, NModal, NInput, NInputGroup, NInputGroupLabel, NCard } from 'naive-ui'
    import { useDialog } from 'naive-ui'
    import type { MessageReactive } from 'naive-ui'
    import { FingerPrint } from '@vicons/ionicons5'
    import { webauthnAuthentication, webauthnRegister } from '@/utils/webauthn'
    import { notyf } from '@/utils/notyf'
    import { useUserStateStore } from '@/stores/userStateStore'
    import { MossyApiError } from '@/utils/apiCall'
    import { useWindowSize } from '@vueuse/core'
    import { useRouter, useRoute } from 'vue-router'


    const userStateStore = useUserStateStore()
    const { width } = useWindowSize()
    const small_device = computed(() => width.value < 768)
    let messageReactive: MessageReactive | null = null
    const message = useMessage()
    const router = useRouter()
    const route = useRoute()
    const dialog = useDialog()
    const showReg = ref(false)
    const { t } = useI18n()
    const login = async () => {
        await webauthnAuthentication()
            .then(() => {
                router.push('/home')
            })
            .catch((err) => {
                notyf.error(t(`api.statusmsg.${err.message}.notification`))
            })

    }
    const username = ref('')
    const usernameInputDisable = ref(false)
    const ServiceUrl = new URL(import.meta.env.VITE_BASE_URL || window.location.href)
    const register = async () => {
        usernameInputDisable.value = true
        createMessage()
        await webauthnRegister(username.value)
            .then((r_key) => {
                notyf.success(t('ui.setup_page.AllDone'))
                showReg.value = false
                if (r_key && r_key != '') {
                    dialog.success({
                        title: t('ui.common_desc.registerFinish'),
                        content: () => h('div', {}, [
                            h('p', t('ui.common_desc.save_key')),
                            h('code', { class: 'text-xl' }, r_key.toString())
                        ]),
                        positiveText: t('ui.common_desc.done'),
                        onPositiveClick: () => {
                            login()
                            return true
                        }
                    })
                }
                else {
                    login()
                }
            })
            .catch((e) => {
                notyf.error(t(`api.statusmsg.${e.message}.notification`))
            })
            .finally(() => {
                removeMessage()
                usernameInputDisable.value = false
            })
    }
    const removeMessage = () => {
        if (messageReactive) {
            messageReactive.destroy()
            messageReactive = null
        }
    }
    const createMessage = () => {
        messageReactive = message.loading(t('ui.setup_page.on_processing'), {
            duration: 0
        })
    }
    const inputCheck = (value: string): boolean => {
        if (value.length === 0) {
            return true
        }
        const urlSafeRegex = /^[A-Za-z0-9\-_]+$/;
        if (urlSafeRegex.test(value)) {
            return true
        } else {
            return false
        }
    }


    onBeforeUnmount(removeMessage)
</script>

<template>
    <n-flex :vertical="!small_device" class="mx-2 md:mx-0">
        <p class="p-0 m-0 hidden md:block">
            {{ t('ui.leftsider.loginandreg.desc') }}
        </p>
        <p class="p-0 m-0 font-bold hidden md:block">
            {{ t('ui.leftsider.loginandreg.saftyfirst') }}
        </p>
        <n-button round :size="!small_device ? 'large' : 'medium'" type="primary" @click="showReg = true">
            {{ t('ui.common_desc.register') }}
        </n-button>
        <n-button round :size="!small_device ? 'large' : 'medium'" strong ghost type="primary" @click="login">
            <template #icon>
                <n-icon>
                    <FingerPrint />
                </n-icon>
            </template>
            {{ t('ui.common_desc.login') }}
        </n-button>
        <n-modal v-model:show="showReg" preset="card" :title="t('ui.common_desc.register')"
            class="w-11/12 md:w-1/2 max-w-xl">
            <n-input-group>
                <n-input-group-label size="large">@</n-input-group-label>
                <n-input v-model:value="username" :placeholder="t('ui.common_desc.inputUsername')" maxlength="32"
                    show-count clearable :disabled="usernameInputDisable" :allow-input="inputCheck" size="large">
                </n-input>
                <n-input-group-label size="large" class="hidden md:block">{{ ServiceUrl.host }}</n-input-group-label>
            </n-input-group>
            <template #footer>
                {{ t('ui.common_desc.usernameAllow') }}
            </template>
            <template #action>
                <n-button round type="primary" size="large" :loading="usernameInputDisable" @click="register">
                    {{ t('ui.common_desc.submit') }}
                </n-button>
            </template>
        </n-modal>
    </n-flex>
</template>