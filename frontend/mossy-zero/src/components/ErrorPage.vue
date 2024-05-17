<script setup lang="ts">
    import { useI18n } from 'vue-i18n'
    import { NButton, NResult, NCard } from 'naive-ui'

    defineProps<{
        msg: string
    }>()

    const { t } = useI18n()
    const goHome = () => {
        window.location.href = '/'
    }
</script>

<template>
    <div class="mt-16 sm:mt-20 md:mt-28 lg:mt-40 xl:mt-52">
        <n-result status="500" :title="t(`api.statusmsg.${msg}.title`)"
            :description="t(`api.statusmsg.${msg}.content`)">
            <template #footer>
                <n-button @click="goHome">{{ t('ui.common_desc.go_home') }}</n-button>
            </template>
        </n-result>
    </div>
</template>