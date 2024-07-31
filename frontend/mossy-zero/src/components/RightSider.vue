<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import { RouterView } from 'vue-router'
    import { useI18n } from 'vue-i18n'
    import { NFlex } from 'naive-ui'
    import { useMessage } from 'naive-ui'
    import UserProfileCard from './common/UserProfileCard.vue'
    import NormalStatusEditor from './common/NormalStatusEditor.vue'
    import { useUserStateStore } from '@/stores/userStateStore'
    import { parseJWT } from '@/utils/jwtParser'
    import { callMossyApi, MossyApiError } from '@/utils/apiCall'
    import { notyf } from '@/utils/notyf'

    interface Avatar {
        file_content?: string; // Base64 encoded content of the avatar file
        file_type?: string; // MIME type of the avatar file
        file_size: number; // Size of the avatar file in bytes
    }

    interface Header {
        file_content?: string; // Base64 encoded content of the header file
        file_type?: string; // MIME type of the header file
        file_size: number; // Size of the header file in bytes
    }

    interface UserProfile {
        uid: string;
        display_name: string; // Display name of the user
        desc: string; // Description of the user
        avatar: Avatar; // Avatar of the user
        header: Header; // Header of the user
        fields: Array<Partial<Record<string, any>>>; // List of additional fields
    }

    const message = useMessage()
    const { t } = useI18n()
    const userStateStore = useUserStateStore()
    const user_info = ref<UserProfile>({
        uid: "123",
        display_name: "John Doe",
        desc: "",
        avatar: {
            file_content: "base64-data-here",
            file_type: "image/png",
            file_size: 0
        },
        header: {
            file_content: "",
            file_type: "",
            file_size: 0
        },
        fields: []
    })
    const user_avatar = ref<string>('')

    const fetch_user = callMossyApi({
        endpoint: '/api/m1/user/profile',
        method: "GET"
    }).then((res) => {
        console.log(res)
        user_info.value = res
        user_avatar.value = `data:${res.avatar.file_type};base64,${res.avatar.file_content}`
    }).catch((e: MossyApiError) => {
        console.error(e)
        notyf.error(t(`api.error_msg.${e.type}.${e.category}.${e.detail}`))
    })

    onMounted(() => {
        if (userStateStore.isLoggedIn) {
            fetch_user
        }
    })
</script>

<template>
    <n-flex vertical v-if="userStateStore.isLoggedIn">
        <UserProfileCard :name="user_info!.display_name" :uid="user_info!.uid" :avatar="user_avatar" />
        <NormalStatusEditor />
    </n-flex>
    <n-flex vertical>
        222
    </n-flex>
</template>