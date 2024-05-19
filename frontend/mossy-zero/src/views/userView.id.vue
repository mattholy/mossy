<script setup lang="ts">
    import { ref } from 'vue'
    import { NFlex, NButton, NIcon, NImage, NAvatar, NThing, NTime, NDescriptions, NDescriptionsItem, NTag, NTabs, NTab } from 'naive-ui'
    import { useRoute, useRouter } from 'vue-router'
    import { NotificationsOutline, CalendarOutline } from '@vicons/ionicons5'
    import { useI18n } from 'vue-i18n'
    import SubpageHeader from '@/components/support/SubpageHeader.vue'
    import { parseJWT } from '@/utils/jwtParser'
    import { useUserStateStore } from '@/stores/userStateStore'
    import { RouterView } from 'vue-router'

    const route = useRoute()
    const router = useRouter()
    const { t } = useI18n()
    const username = route.params.id as string
    const userStateStore = useUserStateStore()
    const html = ref(`
    <p>你首页最充满电量的阿喵。四处乱电，Fediverse知名疯言疯语。关心一切，包括你死后的墓碑。<br />别介意，我并不歧视任何人。但是性别带来歧视，所以请和我一同支持零元性别。</p>
                <p>大部分嘟文内容没有意义，少部分充满哲理。兴许人的一生亦是如此。</p>
                <p>Panromantic / Demisexual<br />积极refo&amp;unfo，动力十足</p>
                <p>存在以下内容，不适合未满18岁UU关注：<br /><a href="https://social.kryta.app/tags/%E6%B8%B8%E6%88%8F"
                        class="mention hashtag" rel="tag">#<span>游戏</span></a> <a
                        href="https://social.kryta.app/tags/NSFW" class="mention hashtag"
                        rel="tag">#<span>NSFW</span></a> <a href="https://social.kryta.app/tags/%E9%94%AE%E6%94%BF"
                        class="mention hashtag" rel="tag">#<span>键政</span></a> <a
                        href="https://social.kryta.app/tags/%E7%89%87%E9%9D%A2%E7%9A%84%E8%AE%BA%E6%96%AD"
                        class="mention hashtag" rel="tag">#<span>片面的论断</span></a> <a
                        href="https://social.kryta.app/tags/%E6%90%9E%E9%BB%84%E8%89%B2" class="mention hashtag"
                        rel="tag">#<span>搞黄色</span></a></p>
                        `)
</script>

<template>
    <SubpageHeader pageCategory="user" />
    <n-flex>
        <n-image width="100%"
            src="https://social.kryta.app/system/site_uploads/files/000/000/001/@2x/f5b2eaf823221de8.png" />
        <div class="-mt-12 px-4 w-full">
            <n-flex justify="space-between" class="w-full items-end">
                <n-avatar round :size="100" src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg" />
                <n-descriptions class="text-center" label-align="center" label-class="w-20">
                    <n-descriptions-item>
                        <template #label>
                            <span class="text-lg font-mono">1231233</span>
                        </template>
                        <span class="text-base">{{ t('ui.pages.actor_detail.activities_count') }}</span>
                    </n-descriptions-item>
                    <n-descriptions-item>
                        <template #label>
                            <span class="text-lg font-mono">123123</span>
                        </template>
                        <span class="text-base">{{ t('ui.pages.actor_detail.following_count') }}</span>
                    </n-descriptions-item>
                    <n-descriptions-item>
                        <template #label>
                            <span class="text-lg font-mono">123123</span>
                        </template>
                        <span class="text-base">{{ t('ui.pages.actor_detail.follower_count') }}</span>
                    </n-descriptions-item>
                </n-descriptions>
            </n-flex>
            <div>
                <n-thing class="my-2">
                    <template #header>
                        <span class="text-xl font-semibold p-0 m-0">07akioni</span>
                    </template>
                    <template #header-extra>
                        <n-flex v-if="userStateStore.isLoggedIn">
                            <n-button round size="large" ghost type="primary" strong
                                v-if="`@${parseJWT(userStateStore.token as string).payload.sub}` == username"
                                @click="router.push('/settings/personal')"> {{ t('ui.pages.actor_detail.change_profile')
                                }}
                            </n-button>
                            <n-button round size="large" ghost type="primary" strong
                                v-if="`@${parseJWT(userStateStore.token as string).payload.sub}` != username"> 关注
                            </n-button>
                            <n-button circle size="large" ghost type="primary" strong
                                v-if="`@${parseJWT(userStateStore.token as string).payload.sub}` != username">
                                <n-icon>
                                    <NotificationsOutline />
                                </n-icon>
                            </n-button>
                        </n-flex>
                    </template>
                    <template #description>
                        <span class="font-sans p-0 m-0">@123@123.com</span>
                    </template>
                    <template #footer>
                        <n-tag round :bordered="false">
                            {{ t('ui.pages.actor_detail.reg_time') }} | <n-time :to="Date.now()" type="date" />
                            <template #icon>
                                <n-icon>
                                    <CalendarOutline />
                                </n-icon>
                            </template>
                        </n-tag>
                    </template>
                </n-thing>
                <v-md-preview-html :html="html" preview-class="vuepress-markdown-body"></v-md-preview-html>
            </div>
            <div class="py-4">
                <n-descriptions bordered :column="1" label-placement="left" size="small">
                    <n-descriptions-item>
                        <template #label>
                            <span class="truncate">zhceshij</span>
                        </template>
                        <span class="truncate">苹果asdfasdflajsd ;lfkja sdl;k</span>
                    </n-descriptions-item>
                </n-descriptions>
            </div>
            <n-tabs type="segment">
                <n-tab name="幸福">
                    寂寞围绕着电视
                </n-tab>
                <n-tab name="的">
                    垂死坚持
                </n-tab>
                <n-tab name="旁边">
                    在两点半消失
                </n-tab>
            </n-tabs>
            <RouterView />
        </div>
    </n-flex>
</template>
<style scoped>
    .long-text {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-left: 10px;
    }
</style>