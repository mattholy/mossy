<script setup lang="ts">
    import { ref } from 'vue'
    import { useRouter, useRoute } from 'vue-router'
    import { callMossyApi, MossyApiError } from './utils/apiCall'
    import { useThemeStore } from '@/stores/themeStore'
    import { useUserStateStore } from '@/stores/userStateStore'
    import { useI18n } from 'vue-i18n'
    import { NFlex, NResult, NButton, NThing, NAvatar, NListItem, NList, NIcon, NCard, NModal } from 'naive-ui'
    import { ArrowForward, Close } from '@vicons/ionicons5'
    import parseOAuthScopes from '@/utils/scopeParse'
    import { webauthnAuthentication } from '@/utils/webauthn'
    import { notyf } from './utils/notyf'
    import AuthSection from '@/components/support/AuthSection.vue'

    const userStateStore = useUserStateStore()
    const route = useRoute()
    const router = useRouter()
    const { t, te } = useI18n()
    const login = () => {
        webauthnAuthentication()
            .then((res) => { })
            .catch((err) => {
                notyf.error(t(`api.statusmsg.${err.message}.notification`))
            })
    }
</script>

<template>
    <n-flex justify="center" class="w-full">
        <n-card embedded class="m-10 p-4 max-w-xl">
            <n-result status="info" :title="t('ui.pages.oauth.title')">
                <n-flex vertical>
                    <n-thing class="p-4">
                        <template #header>
                            {{ route.query.client_name }}
                        </template>
                        <template #description>
                            {{ t(`ui.pages.oauth.request`) }}
                        </template>
                        <n-list>
                            <n-list-item v-for="scope in String(route.query.scope).split(' ')" :key="scope">
                                <template #prefix>
                                    <n-icon>
                                        <ArrowForward v-if="te(`ui.pages.oauth.scopes_desc.${scope}`)" />
                                        <Close v-else />
                                    </n-icon>
                                </template>
                                <template #default>
                                    {{
                                        te(`ui.pages.oauth.scopes_desc.${scope}`) ? t(`ui.pages.oauth.scopes_desc.${scope}`)
                                            :
                                            t(`ui.pages.oauth.unkown_scope`) + scope
                                    }}
                                </template>
                            </n-list-item>
                        </n-list>
                        <template #action>
                            {{ t(`ui.pages.oauth.not_mossy`) }}
                        </template>
                    </n-thing>
                    <n-thing class="p-4" v-if="userStateStore.isLoggedIn">
                        <template #avatar>
                            <n-avatar round :size='50'
                                src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg" />
                        </template>
                        <template #header>
                            头像33
                        </template>
                        <template #description>
                            头像发士大夫艰苦
                        </template>
                        <template #header-extra>
                            <span class="cursor-pointer" @click="login">
                                {{ t(`ui.pages.oauth.switch_acc`) }}
                            </span>
                        </template>
                        <template #action>
                            {{ t(`ui.pages.oauth.permission_by_mossy`) }}
                        </template>
                    </n-thing>
                </n-flex>
                <template #footer>
                    <n-flex justify="space-evenly" v-if="userStateStore.isLoggedIn">
                        <n-button type="primary" round strong size="large">
                            {{ t(`ui.pages.oauth.grant`) }}
                        </n-button>
                        <n-button type="error" round strong size="large">
                            {{ t(`ui.pages.oauth.deny`) }}
                        </n-button>
                    </n-flex>
                    <n-flex justify="space-evenly" v-else>
                        <n-flex vertical>
                            <p>{{ t(`ui.pages.oauth.goin_with_login`) }}</p>
                            <AuthSection />
                        </n-flex>
                    </n-flex>
                </template>
            </n-result>
        </n-card>
    </n-flex>
</template>