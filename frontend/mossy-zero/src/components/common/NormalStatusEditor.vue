<script setup lang="ts">
    import { NButton, NInput, NFlex, NUpload, NCollapseItem, NCollapse, NIcon } from 'naive-ui';
    import { ImageOutline, LockOpen, LockClosed, AtCircle, LocationOutline, Location, LanguageOutline, WarningOutline, EarthOutline } from '@vicons/ionicons5'
</script>
<template>
    <n-input placeholder="内容警告" show-count :maxlength="99" />
    <n-input type="textarea" placeholder="想说些什么？输入@来提及别人，输入#来引用Tag，输入:来使用表情" show-count :maxlength="5000"
        :autosize="{ minRows: 4, maxRows: 12 }" />
    <n-flex class="px-2">
        <n-button text>
            <template #icon>
                <n-icon>
                    <EarthOutline />
                </n-icon>
            </template>
        </n-button>
        <n-button text>
            <template #icon>
                <n-icon>
                    <WarningOutline />
                </n-icon>
            </template>
        </n-button>
        <n-button text>
            <template #icon>
                <n-icon>
                    <LocationOutline />
                </n-icon>
            </template>
        </n-button>
        <n-button text>
            <template #icon>
                <n-icon>
                    <LanguageOutline />
                </n-icon>
            </template>
            简体中文
        </n-button>
    </n-flex>
    <n-collapse>
        <n-collapse-item>
            <template #header>
                <n-icon>
                    <ImageOutline />
                </n-icon>
                <span class="px-1">添加媒体</span>
            </template>
            <template #header-extra>
                <span class="px-1">已添加 0/9</span>
            </template>
            <n-upload action="https://www.mocky.io/v2/5e4bafc63100007100d8b70f" list-type="image-card"
                accept="image/*, video/*" />
        </n-collapse-item>
    </n-collapse>
    <n-button type="primary" round class="mx-2">
        发布
    </n-button>
</template>