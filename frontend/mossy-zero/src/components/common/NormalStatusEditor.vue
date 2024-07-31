<script setup lang="ts">
    import { ref, nextTick } from 'vue'
    import { NButton, NInput, NFlex, NUpload, NCollapseItem, NCollapse, NIcon, NIconWrapper, NCollapseTransition } from 'naive-ui';
    import { ImageOutline, LockOpen, LockClosed, AtCircle, LocationOutline, Location, LanguageOutline, WarningOutline, EarthOutline, Warning } from '@vicons/ionicons5'
    import type { InputInst } from 'naive-ui'

    const showCW = ref<boolean>(false)
    const inputInstRef = ref<InputInst | undefined>(undefined)

    const toggleCW = () => {
        showCW.value = !showCW.value
        if (showCW.value) {
            nextTick(() => inputInstRef.value?.focus())
        } else {
            inputInstRef.value?.blur()
        }
    }
</script>

<template>
    <n-flex class="px-2">
        <n-collapse-transition :show="showCW">
            <n-input ref="inputInstRef" placeholder="内容警告" show-count :maxlength="99" />
        </n-collapse-transition>
        <n-input type="textarea" placeholder="想说些什么？输入@来提及别人，输入#来引用Tag，输入:来使用表情" show-count :maxlength="5000"
            :autosize="{ minRows: 4, maxRows: 12 }" />
        <n-flex class="px-2">
            <n-button text @click="toggleCW">
                <template #icon>
                    <n-icon v-if="!showCW">
                        <WarningOutline />
                    </n-icon>
                    <n-icon color="#f00" v-else>
                        <Warning />
                    </n-icon>
                </template>
            </n-button>
            <n-button text>
                <template #icon>
                    <n-icon>
                        <EarthOutline />
                    </n-icon>
                </template>
            </n-button>
            <!-- <n-button text>
                <template #icon>
                    <n-icon>
                        <LocationOutline />
                    </n-icon>
                </template>
            </n-button> -->
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
        <n-button type="primary" round class="w-full">
            发布
        </n-button>
    </n-flex>
</template>