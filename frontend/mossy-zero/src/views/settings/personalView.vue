<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import { NForm, NFormItem, NImage, NFlex, NInput, NUpload, NUploadDragger, NIcon, NDynamicInput } from 'naive-ui';
    import { FileTray } from '@vicons/ionicons5'
    import { useI18n } from 'vue-i18n';
    import type {
        UploadOnChange,
        FormRules,
        UploadFileInfo
    } from 'naive-ui'
    import { notyf } from '@/utils/notyf';

    type ImageType = 'avatar' | 'header'

    const { t } = useI18n()
    const form_data = ref({
        "display_name": "John Doe",
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

    const rules: FormRules = {}

    const handleAvatar: UploadOnChange = (payload) => {
        if (payload.fileList.length != 0) {
            const listedFile = payload.fileList.pop()
            if (listedFile == undefined) {
                return
            }
            const file = listedFile.file as File
            if (file.size > 5 * 1024 * 1024) {
                notyf.error(t('ui.pages.settings.personal.basic_info.avatar.file_too_large'));
                return
            }

            const reader = new FileReader();

            reader.onload = (event) => {
                const base64String = (event.target?.result as string).split(',')[1];
                form_data.value.avatar = {
                    "file_content": base64String,
                    "file_type": file.type,
                    "file_size": file.size
                };

                console.log(form_data.value.avatar);
            };

            reader.onerror = (error) => {
                console.error("Error reading file:", error);
            };

            reader.readAsDataURL(file);
        }
    }

    const handleHeader: UploadOnChange = (payload) => {
        if (payload.fileList.length != 0) {
            const listedFile = payload.fileList.pop()
            if (listedFile == undefined) {
                return
            }
            const file = listedFile.file as File
            if (file.size > 10 * 1024 * 1024) {
                console.log(t('ui.pages.settings.personal.basic_info.header.file_too_large'));
                return;
            }

            const reader = new FileReader();

            reader.onload = (event) => {
                const base64String = (event.target?.result as string).split(',')[1];
                form_data.value.header = {
                    "file_content": base64String,
                    "file_type": file.type,
                    "file_size": file.size
                };

                console.log(form_data.value.avatar);
            };

            reader.onerror = (error) => {
                console.error("Error reading file:", error);
            };

            reader.readAsDataURL(file);
        }
    }
</script>
<template>
    <n-form :model="form_data" size="large">
        <n-form-item path="display_name">
            <template #label>
                <p class="p-0 m-0 font-bold text-base">{{ t('ui.pages.settings.personal.basic_info.display_name.label')
                    }}</p>
                <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.display_name.instruction') }}</p>
            </template>
            <n-input v-model:value="form_data.display_name"
                :placeholder="t('ui.pages.settings.personal.basic_info.display_name.placeholder')" show-count
                :maxlength="30" clearable />
        </n-form-item>
        <n-form-item path="desc">
            <template #label>
                <p class="p-0 m-0 font-bold text-base">{{ t('ui.pages.settings.personal.basic_info.desc.label')
                    }}</p>
                <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.desc.instruction', {
                    user: '@其他人', tag:
                        '#标签'
                }) }}</p>
            </template>
            <n-input v-model:value="form_data.desc"
                :placeholder="t('ui.pages.settings.personal.basic_info.desc.placeholder')" type="textarea"
                :autosize="{ minRows: 3 }" show-count :maxlength="500" clearable />
        </n-form-item>
        <n-form-item path="avatar">
            <template #label>
                <p class="p-0 m-0 font-bold text-base">{{ t('ui.pages.settings.personal.basic_info.avatar.label')
                    }}</p>
                <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.avatar.instruction') }}</p>
            </template>
            <n-upload :show-preview-button="true" :default-upload="false" list-type="image" :max="1" accept="image/*"
                v-model:value="form_data.avatar" @change="handleAvatar" name='qqqqqqqqqqqqqq'>
                <n-upload-dragger>
                    <div v-if="form_data.avatar.file_content == ''">
                        <n-icon size="32">
                            <FileTray />
                        </n-icon>
                        <p class="p-0 m-0 font-bold text-base">{{ t('ui.common_desc.drag_to_upload') }}</p>
                        <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.avatar.placeholder') }}</p>
                    </div>
                    <div v-else>
                        <n-image :height="200" preview-disabled
                            :src="`data:${form_data.avatar.file_type};base64,${form_data.avatar.file_content}`" />
                        <div>
                            <p class="p-0 m-0 font-bold text-base">
                                {{ t('ui.pages.settings.personal.basic_info.avatar.instruction_for_replace') }}
                            </p>
                            <p class="p-0 m-0">
                                {{ t('ui.pages.settings.personal.basic_info.avatar.placeholder') }}
                            </p>
                        </div>
                    </div>
                </n-upload-dragger>
            </n-upload>
        </n-form-item>
        <n-form-item path="header">
            <template #label>
                <p class="p-0 m-0 font-bold text-base">{{ t('ui.pages.settings.personal.basic_info.header.label')
                    }}</p>
                <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.header.instruction') }}</p>
            </template>
            <n-upload :show-preview-button="true" :default-upload="false" list-type="image" :max="2" accept="image/*"
                v-model:value="form_data.avatar" @change="handleHeader">
                <n-upload-dragger>
                    <div v-if="form_data.header.file_content == ''">
                        <n-icon size="32">
                            <FileTray />
                        </n-icon>
                        <p class="p-0 m-0 font-bold text-base">{{ t('ui.setup_page.server_banner.instruction') }}</p>
                        <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.header.placeholder') }}</p>
                    </div>
                    <div v-else>
                        <n-image :height="200" preview-disabled
                            :src="`data:${form_data.header.file_type};base64,${form_data.header.file_content}`" />
                        <div>
                            <p class="p-0 m-0 font-bold text-base">
                                {{ t('ui.pages.settings.personal.basic_info.header.instruction_for_replace') }}
                            </p>
                            <p class="p-0 m-0">
                                {{ t('ui.pages.settings.personal.basic_info.header.placeholder') }}
                            </p>
                        </div>
                    </div>
                </n-upload-dragger>
            </n-upload>
        </n-form-item>
        <n-form-item path="fields">
            <template #label>
                <p class="p-0 m-0 font-bold text-base">{{ t('ui.pages.settings.personal.basic_info.fields.label')
                    }}</p>
                <p class="p-0 m-0">{{ t('ui.pages.settings.personal.basic_info.fields.instruction') }}</p>
            </template>
            <n-dynamic-input v-model:value="form_data.fields" :max="6" preset="pair"
                :key-placeholder="t('ui.pages.settings.personal.basic_info.fields.placeholder_left')"
                :value-placeholder="t('ui.pages.settings.personal.basic_info.fields.placeholder_right')" />
        </n-form-item>

    </n-form>
</template>