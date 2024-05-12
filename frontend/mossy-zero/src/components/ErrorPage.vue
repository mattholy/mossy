<script setup lang="ts">
import { defineProps } from 'vue'
import { useI18n } from 'vue-i18n'
import { NButton, NResult, NCard } from 'naive-ui'

interface Props {
    msg: string;
}

const { t } = useI18n()
const props = defineProps<Props>();
const goHome = () => {
    window.location.href = '/'
}
</script>

<template>
    <div class="px-8 py-10 md:px-40 md:py-40 xl:px-96 xl:py-56">
        <n-card :bordered="false" size="huge">
            <n-result status="500" :title="t(`api.statusmsg.${props.msg}.title`)"
                :description="t(`api.statusmsg.${props.msg}.content`)">
                <template #footer>
                    <n-button @click="goHome">{{ t('ui.common_desc.go_home') }}</n-button>
                </template>
            </n-result>
        </n-card>
    </div>
</template>