<script setup lang="ts">
    import { defineProps } from 'vue'

    interface Props {
        content: string;
    }

    const props = defineProps<Props>();
</script>

<template>
    <v-md-preview :text="props.content" preview-class="vuepress-markdown-body"></v-md-preview>
</template>



<style scoped></style>