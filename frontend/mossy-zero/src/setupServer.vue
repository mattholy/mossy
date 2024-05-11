<script setup lang="ts">
import { defineComponent, ref } from 'vue'
import { NButton, NCard, NForm, NFormItem, NInput, NInputGroup, NInputGroupLabel, NUpload, NSwitch, NUploadDragger, NP, NText, NIcon } from 'naive-ui'
import { type FormInst, type FormRules, type FormItemRule, type UploadOnChange } from 'naive-ui'
import { useI18n } from 'vue-i18n'
import { FileTray } from '@vicons/ionicons5'
import { MossySetupService } from '@/client/services.gen'
import { type SetupStatusSetupInitPostData } from '@/client/types.gen'
import { OpenAPI } from '@/client/core/OpenAPI'
import { notyf } from '@/utils/notyf'
import { webauthnRegister } from '@/utils/webauthn'

interface FileDetails {
    file_name: string;
    file_count: number;
    file_size: number;
    file_type: string;
    file_content: string;
    isTwoToOne: boolean;
}

const { t } = useI18n()
const setupForm = ref<FormInst | null>(null)
const setupFormData = ref({
    server_name: '',
    server_desc: '',
    server_admin: '',
    server_service: '',
    server_about: '',
    server_banner: {
        file_name: '',
        file_count: 0,
        file_size: 0,
        file_type: '',
        file_content: '',
        isTwoToOne: false
    },
    server_status: '',
    server_isolated: false,
    server_telemetry: true,
    server_union: true
})



const ServiceUrl = new URL(import.meta.env.VITE_BASE_URL || window.location.href)

const setupServer = async () => {
    setupForm.value?.validate().then(() => {
        MossySetupService.setupStatusSetupInitPost(
            {
                requestBody: {
                    server_name: setupFormData.value.server_name,
                    server_desc: setupFormData.value.server_desc,
                    server_admin: setupFormData.value.server_admin,
                    server_service: setupFormData.value.server_service,
                    server_about: setupFormData.value.server_about,
                    server_banner: setupFormData.value.server_banner,
                    server_status: setupFormData.value.server_status,
                    server_isolated: setupFormData.value.server_isolated,
                    server_telemetry: setupFormData.value.server_telemetry,
                    server_union: setupFormData.value.server_union
                }
            }
        )
            .then(async (res) => {
                if (res.status === 'OK') {
                    await webauthnRegister(setupFormData.value.server_admin)
                }
            })
            .catch((e) => {
                console.error(e)
                notyf.error(t(`ui.setup_page.${e.message}`))
            })
    })
        .catch((e) => {
            notyf.error(t('ui.setup_page.formError'))
        })
}

const handleImage: UploadOnChange = (payload) => {
    if (payload.fileList.length === 0) {
        setupFormData.value.server_banner.file_count = 0
        setupFormData.value.server_banner.file_size = 0
        setupFormData.value.server_banner.file_type = ''
        setupFormData.value.server_banner.file_name = ''
        setupFormData.value.server_banner.isTwoToOne = false
        setupFormData.value.server_banner.file_content = ''
        return
    } else {
        const firstFile = payload.fileList[0].file;
        if (!firstFile) {
            return;
        }
        setupFormData.value.server_banner.file_count = payload.fileList.length
        setupFormData.value.server_banner.file_size = firstFile.size
        setupFormData.value.server_banner.file_type = firstFile.type
        setupFormData.value.server_banner.file_name = firstFile.name
        const reader = new FileReader();
        reader.onload = (event: ProgressEvent<FileReader>) => {
            const img = new Image();
            img.onload = () => {
                const aspectRatio = img.width / img.height;
                if (Math.abs(aspectRatio - 2) < 0.1) {
                    setupFormData.value.server_banner.isTwoToOne = true
                    if (event.target?.result) {
                        const base64Content = event.target.result.toString();
                        setupFormData.value.server_banner.file_content = base64Content
                    }
                } else {
                    setupFormData.value.server_banner.isTwoToOne = false
                }
            };
            img.onerror = () => {
                console.error('Error loading image.');
            };
            if (event.target?.result) {
                img.src = event.target.result.toString();
            }
        };
        reader.onerror = (error) => {
            console.error('Error reading file:', error);
        };
        reader.readAsDataURL(firstFile);
    }
}

const rules: FormRules = {
    server_name: [
        {
            required: true,
            validator(rule: FormItemRule, value: string) {
                if (!value) {
                    return new Error(t('ui.setup_page.server_name.requiredError'))
                }
                return true
            },
            trigger: ['input', 'blur']
        }
    ],
    server_desc: [],
    server_admin: [
        {
            required: true,
            validator(rule: FormItemRule, value: string) {
                if (!value) {
                    return new Error(t('ui.setup_page.server_admin.requiredError'))
                }
                return true
            },
            trigger: ['input', 'blur']
        }
    ],
    server_service: [
        {
            validator(rule: FormItemRule, value: string) {
                if (value) {
                    try {
                        new URL(value);
                        return true
                    } catch (e) {
                        return new Error(t('ui.setup_page.server_service.urlError'))
                    }
                }
                return true
            },
            trigger: ['input', 'blur']
        }
    ],
    server_about: [],
    server_banner: [
        {
            validator(rule: FormItemRule, value: FileDetails) {
                if (value.file_count > 0) {
                    if (value.file_count != 1) {
                        return new Error(t('ui.setup_page.server_banner.fileCountError'))
                    }
                    if (!value.isTwoToOne) {
                        return new Error(t('ui.setup_page.server_banner.aspectRatioError'))
                    }
                }
                return true
            },
            trigger: ['input', 'blur']
        }
    ],
    server_status: [
        {
            validator(rule: FormItemRule, value: string) {
                if (value) {
                    try {
                        new URL(value);
                        return true
                    } catch (e) {
                        return new Error(t('ui.setup_page.server_status.urlError'))
                    }
                }
                return true
            },
            trigger: ['input', 'blur']
        }
    ]
}

</script>

<template>
    <div class="px-2 py-4 md:px-24 md:py-24 lg:px-32 lg:py-32 xl:px-96 xl:py-56">
        <n-card header-class="sticky top-12 z-30 font-bold bg-opacity-30 backdrop-filter backdrop-blur-md" :segmented="{
            content: true,
            footer: 'soft'
        }">
            <template #header>
                {{ t('ui.setup_page.title') }}
            </template>
            <template #header-extra>
                {{ t('ui.setup_page.title-extra') }}
            </template>
            <n-form ref="setupForm" :model="setupFormData" :rules="rules">
                <n-form-item :label="t('ui.setup_page.server_name.label')" path="server_name">
                    <n-input v-model:value="setupFormData.server_name"
                        :placeholder="t('ui.setup_page.server_name.placeholder')" maxlength="64" show-count clearable />
                </n-form-item>
                <n-form-item :label="t('ui.setup_page.server_desc.label')" path="server_desc">
                    <n-input v-model:value="setupFormData.server_desc"
                        :placeholder="t('ui.setup_page.server_desc.placeholder')" maxlength="512" show-count
                        clearable />
                </n-form-item>
                <n-form-item :label="t('ui.setup_page.server_admin.label')" path="server_admin">
                    <n-input-group>
                        <n-input-group-label>@</n-input-group-label>
                        <n-input v-model:value="setupFormData.server_admin"
                            :placeholder="t('ui.setup_page.server_admin.placeholder')" maxlength="32" show-count
                            clearable />
                        <n-input-group-label>@{{ ServiceUrl.host }}</n-input-group-label>
                    </n-input-group>
                </n-form-item>
                <n-form-item :label="t('ui.setup_page.server_service.label')" path="server_service">
                    <n-input v-model:value="setupFormData.server_service"
                        :placeholder="t('ui.setup_page.server_service.placeholder')" maxlength="512" show-count
                        clearable />
                </n-form-item>
                <n-form-item :label="t('ui.setup_page.server_about.label')" path="server_content">
                    <n-input v-model:value="setupFormData.server_about"
                        :placeholder="t('ui.setup_page.server_about.placeholder')" type="textarea" maxlength="5000"
                        show-count clearable :autosize="{ minRows: 3 }" />
                </n-form-item>
                <n-form-item :label="t('ui.setup_page.server_banner.label')" path="server_banner">
                    <n-upload :show-preview-button="true" :default-upload="false" list-type="image" :max="1"
                        file-list-class="preview" accept="image/*" v-model:value="setupFormData.server_banner"
                        @change="handleImage">
                        <n-upload-dragger>
                            <n-icon size="32">
                                <FileTray />
                            </n-icon>
                            <p class="text-base">{{ t('ui.setup_page.server_banner.instruction') }}</p>
                            <p class="text-sm py-2">{{ t('ui.setup_page.server_banner.placeholder') }}</p>
                        </n-upload-dragger>
                    </n-upload>
                </n-form-item>
                <n-form-item :label="t('ui.setup_page.server_status.label')" path="server_status">
                    <n-input v-model:value="setupFormData.server_status"
                        :placeholder="t('ui.setup_page.server_status.placeholder')" maxlength="512" show-count
                        clearable />
                </n-form-item>
                <n-form-item :label="t('ui.setup_page.server_isolated.label')" path="server_isolated">
                    <n-switch v-model:value="setupFormData.server_isolated" />
                    <p class="text-xs px-2">{{ t('ui.setup_page.server_isolated.placeholder') }}</p>
                </n-form-item>
                <n-form-item :label="t('ui.setup_page.server_telemetry.label')" path="server_telemetry">
                    <n-switch v-model:value="setupFormData.server_telemetry" />
                    <p class="text-xs px-2">{{ t('ui.setup_page.server_telemetry.placeholder') }}</p>
                </n-form-item>
                <n-form-item :label="t('ui.setup_page.server_union.label')" path="server_union">
                    <n-switch v-model:value="setupFormData.server_union" />
                    <p class="text-xs px-2">{{ t('ui.setup_page.server_union.placeholder') }}</p>
                </n-form-item>
            </n-form>
            <template #footer>
                <n-button type="primary" @click="setupServer">
                    {{ t('ui.setup_page.submit') }}
                </n-button>
            </template>
            <template #action>
                {{ t('ui.setup_page.footer') }}
                <a>{{ t('ui.setup_page.ua') }}</a>
                <a>{{ t('ui.setup_page.privacy') }}</a>
            </template>
        </n-card>
    </div>
</template>

<style scoped>
.preview {
    width: 200px !important;
    height: 100px !important;
}
</style>