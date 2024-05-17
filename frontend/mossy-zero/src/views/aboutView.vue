<script setup lang="ts">
    import { ref, computed, onMounted, onUnmounted } from 'vue'
    import { useWindowSize } from '@vueuse/core'
    import { useI18n } from 'vue-i18n'
    import { NFlex, NImage, NCard, NIcon, NGrid, NGridItem, NButton, NCollapseTransition, c } from 'naive-ui';
    import { ChevronDown, EllipsisHorizontal } from '@vicons/ionicons5'
    import UserCard from '@/components/common/UserProfileCard.vue'
    import MarkdownViewer from '@/components/support/MarkdownViewer.vue'
    import { callMossyApi } from '@/utils/apiCall'

    const { t } = useI18n()
    const { width } = useWindowSize();
    const showAbout = ref(true)
    const showRules = ref(false)
    const cols = computed(() => {
        return width.value < 768 ? 1 : 2
    });
</script>

<template>
    <n-flex vertical class="m-0 p-0">
        <n-image lazy src="https://social.kryta.app/system/site_uploads/files/000/000/001/@2x/f5b2eaf823221de8.png"
            preview-disabled width="100%" />
        <div class="text-center p-10">
            <p class="font-bold text-4xl m-0 p-0">Mossy</p>
            <p class="font-normal text-2xl m-0 p-0">a.b.c</p>
            <p class="leading-10 mt-2 p-0">由Mossy驱动的去中心化社交媒体</p>
        </div>
        <div class="mx-2">
            <n-card embedded>
                <n-grid :cols="cols" :collapsed="true" :collapsed-rows="2">
                    <n-grid-item class="flex items-center justify-center">
                        <UserCard name="管理员23423423" uid="root" avatar="" />
                    </n-grid-item>
                    <n-grid-item class="flex items-center justify-center">
                        <n-button round size="large" strong secondary tag="a" href="https://anyway.fm/news.php">
                            {{ t('ui.pages.about.serverContactBtn') }}
                        </n-button>
                    </n-grid-item>
                </n-grid>
            </n-card>
        </div>
        <div class="mx-2">
            <n-card embedded>
                <div class="font-bold cursor-pointer items-center text-center" @click="showAbout = !showAbout">
                    <p class="text-lg m-2">{{ t('ui.pages.about.serverAboutSection') }}</p>
                    <n-icon size="30">
                        <EllipsisHorizontal v-if="!showAbout" />
                        <ChevronDown v-else />
                    </n-icon>
                </div>
                <n-collapse-transition :show="showAbout">
                    <n-card>
                        <MarkdownViewer />
                    </n-card>
                </n-collapse-transition>
            </n-card>
        </div>
        <div class="mx-2 mb-2">
            <n-card embedded>
                <div class="font-bold cursor-pointer items-center text-center" @click="showRules = !showRules">
                    <p class="text-lg  m-2">{{ t('ui.pages.about.serverRuleSection') }}</p>
                    <n-icon size="30">
                        <EllipsisHorizontal v-if="!showRules" />
                        <ChevronDown v-else />
                    </n-icon>
                </div>
                <n-collapse-transition :show="showRules">
                    <n-card>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                        <p>asdasds</p>
                    </n-card>
                </n-collapse-transition>
            </n-card>
        </div>
    </n-flex>

</template>