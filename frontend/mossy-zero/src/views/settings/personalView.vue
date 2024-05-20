<script setup lang="ts">
    import { ref, onMounted, provide } from 'vue'
    import { callMossyApi, type MossyApiError } from '@/utils/apiCall';
    import PersonalDataUpdater from '@/components/support/PersonalDataUpdater.vue';

    interface Avatar {
        file_content: string;
        file_type: string;
        file_size: number;
    }

    interface Header {
        file_content: string;
        file_type: string;
        file_size: number;
    }

    interface Field {
        name: string;
        value: string;
    }

    interface FormData {
        display_name: string;
        desc: string;
        avatar: Avatar;
        header: Header;
        fields: Field[];
    }

    const formData = ref<FormData>({
        "display_name": "",
        "desc": "",
        "avatar": {
            "file_content": "",
            "file_type": "",
            "file_size": 0
        },
        "header": {
            "file_content": "",
            "file_type": "",
            "file_size": 0
        },
        "fields": []
    })

    const loading = ref(true)

    onMounted(() => {
        callMossyApi({
            method: 'GET',
            endpoint: '/api/m1/user/profile'
        }).then((response) => {
            formData.value = response
            loading.value = false
        }).catch((error: MossyApiError) => {
            console.error(error);
        })
    })

    provide('formData', formData);
    provide('loading', loading);
</script>
<template>
    <PersonalDataUpdater />
</template>