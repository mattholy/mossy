<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import { NTabs, NTab, NFlex } from 'naive-ui'
    import { useI18n } from 'vue-i18n'
    import { useRouter } from 'vue-router'
    import { RouterView } from 'vue-router'

    const { t } = useI18n()
    const tab_name = ref('personal')
    const router = useRouter()

    onMounted(() => {
        router.push(`/settings/${tab_name.value}`)
    })
</script>
<template>
    <n-tabs class="sticky top-12 backdrop-blur-md px-4 z-40" v-model:value="tab_name" type="line"
        @click="router.push(`/settings/${tab_name}`)">
        <n-tab name="personal">
            {{ t('ui.pages.settings.header.personal') }}
        </n-tab>
        <n-tab name="system">
            {{ t('ui.pages.settings.header.system') }}
        </n-tab>
    </n-tabs>
    <div class="p-4">
        <RouterView />
    </div>


</template>