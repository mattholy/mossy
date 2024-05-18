<script setup lang="ts">
    import { defineProps } from 'vue'
    import { NAlert, NFlex } from 'naive-ui'
    import { useI18n } from 'vue-i18n'


    interface Props {
        rule_no: string;
        rule_content: string;
        updated_at: string;
    }

    const props = defineProps<Props>();
    const { t } = useI18n()

    function convertToLocalTime(isoDateString: string): string {
        console.log(isoDateString);
        const date = new Date(isoDateString);
        return date.toLocaleString(); // 使用默认的本地格式
    }
</script>

<template>
    <n-alert type="success" :title="t('ui.pages.about.updated_at') + convertToLocalTime(props.updated_at)">
        <template #icon>
            {{ props.rule_no }}
        </template>
        {{ props.rule_content }}
    </n-alert>
</template>