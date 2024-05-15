<script setup lang="ts">
import { NFlex, NButton, NIcon, NPopover, NDivider } from 'naive-ui'
import { useRoute, useRouter } from 'vue-router'
import { ChevronBack, ShareSocial, EllipsisHorizontal, HandRight, Warning } from '@vicons/ionicons5'
import { useI18n } from 'vue-i18n'
import { notyf } from '@/utils/notyf'
import { useAuthStore } from '@/stores/AuthStore'

interface Props {
    pageCategory: 'user' | 'activity'
    resourceUri: string;
}

const authStore = useAuthStore()
const props = defineProps<Props>();
const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const uri = route.params.id

const handleShare = async () => {
    if (navigator.share) {
        try {
            // TODO: Add shareable content
            await navigator.share({
                title: '',
                text: '',
                url: ''
            })
        } catch (error) {
            notyf.error(t('ui.header.statusmsg.shareFail'))
        }
    } else {
        notyf.error(t('ui.header.statusmsg.shareApiNotSupported'));
    }
}

const handleBlock = async () => {
    if (!authStore.isLoggedIn) {
        notyf.error(t('ui.common_desc.loginMust'))
        return
    }
    // TODO: Add block functionality
}

const handleReport = async () => {
    if (!authStore.isLoggedIn) {
        notyf.error(t('ui.common_desc.loginMust'))
        return
    }
    // TODO: Add report functionality
}
</script>

<template>
    <n-flex justify="space-between"
        class="z-40 sticky top-0 font-bold bg-opacity-30 backdrop-filter backdrop-blur-md h-12 items-center"
        style="border-bottom: 1px solid grey;">
        <div class="w-2/12 text-left">
            <n-button icon-placement="left" round ghost strong :bordered="false" @click="router.back()">
                <template #icon>
                    <n-icon>
                        <ChevronBack />
                    </n-icon>
                </template>
                <!-- {{ t('ui.common_desc.go_back') }} -->
            </n-button>
        </div>
        <div class="w-7/12 text-center">
            {{ uri }}
        </div>
        <div class="w-2/12 text-right">
            <n-popover trigger="click" placement="bottom">
                <template #trigger>
                    <n-button icon-placement="right" round ghost strong :bordered="false">
                        <template #icon>
                            <n-icon>
                                <EllipsisHorizontal />
                            </n-icon>
                        </template>
                        <!-- {{ t('ui.common_desc.go_back') }} -->
                    </n-button>
                </template>
                <n-flex vertical class="putThemOnLeft">
                    <n-button icon-placement="left" text strong @click="handleShare">
                        <template #icon>
                            <n-icon>
                                <ShareSocial />
                            </n-icon>
                        </template>
                        {{ t('ui.common_desc.share') }}{{ t('ui.common_desc.person') }}
                    </n-button>
                    <n-button type="warning" icon-placement="left" text strong @click="handleBlock">
                        <template #icon>
                            <n-icon>
                                <HandRight />
                            </n-icon>
                        </template>
                        {{ t('ui.common_desc.block') }}
                    </n-button>
                    <n-button type="error" icon-placement="left" text strong @click="handleReport">
                        <template #icon>
                            <n-icon>
                                <Warning />
                            </n-icon>
                        </template>
                        {{ t('ui.common_desc.report') }}
                    </n-button>
                </n-flex>
            </n-popover>
        </div>
    </n-flex>
</template>

<style scoped>
.putThemOnLeft button {
    text-align: left;
    width: fit-content;
}
</style>