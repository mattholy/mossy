<script setup lang="ts">
import { NAvatar, NFlex, NPopover, NCard } from 'naive-ui'
import { useRouter } from 'vue-router'

interface Props {
    name: string;
    uid: string;
    avatar: string;
}

const router = useRouter();
const props = defineProps<Props>();
</script>

<template>
    <n-flex class="p-4 cursor-pointer" @click="router.push(`/user/@${props.uid}`)">
        <n-avatar :size=45 round :src="props.avatar" />
        <div>
            <p class="text-base font-semibold  m-0">{{ props.name }}</p>
            <p class="tracking-wide  m-0">@{{ props.uid }}</p>
        </div>
    </n-flex>
</template>