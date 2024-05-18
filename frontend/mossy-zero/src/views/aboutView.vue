<script setup lang="ts">
    import { ref, computed, onMounted, onUnmounted } from 'vue'
    import { useWindowSize } from '@vueuse/core'
    import { useI18n } from 'vue-i18n'
    import { NStatistic, NNumberAnimation, NFlex, NImage, NCard, NIcon, NGrid, NGridItem, NButton, NCollapseTransition, c } from 'naive-ui';
    import { ChevronDown, EllipsisHorizontal } from '@vicons/ionicons5'
    import UserCard from '@/components/common/UserProfileCard.vue'
    import MarkdownViewer from '@/components/support/MarkdownViewer.vue'
    import { callMossyApi, MossyApiError } from '@/utils/apiCall'
    import ServerRuleCard from '@/components/common/ServerRuleCard.vue'
    import { notyf } from '@/utils/notyf';

    interface Rule {
        content: string;
        order: number;
        updated_at: string;
    }

    interface Mossy {
        title: string;
        admin_id: string;
        admin_name: string;
        admin_avatar: string;
        server_banner: string;
        contact: string;
        users: number;
        users_of_30: number;
        description: string;
        about: string;
        rules: Rule[];
    }

    const { t } = useI18n()
    const { width } = useWindowSize();
    const showAbout = ref(true)
    const showRules = ref(false)
    const cols = computed(() => {
        return width.value < 768 ? 1 : 2
    });
    const host = location.host
    const universe_user_count = ref(0)
    const universe_user_count_30 = ref(0)
    const about_data = ref<Mossy>({
        title: '',
        admin_id: '',
        admin_name: '',
        admin_avatar: '',
        server_banner: '',
        contact: '',
        users: 0,
        users_of_30: 0,
        description: '',
        about: '',
        rules: [],
    })

    onMounted(() => {
        callMossyApi({
            endpoint: '/api/m1/server/info',
            method: 'GET',
        }).then((res) => {
            about_data.value = res
        }).catch((err: MossyApiError) => {
            notyf.error(err.detail)
        })

        fetch('https://api.fedidb.org/v1/stats')
            .then((res) => res.json())
            .then((res) => {
                universe_user_count.value = res.total_users
                universe_user_count_30.value = res.monthly_active_users
            })
            .catch((err) => {
                console.error(err)
            })
    })
</script>

<template>
    <n-flex vertical class="m-0 p-0">
        <n-image lazy :src="about_data.server_banner" preview-disabled width="100%" />
        <div class="text-center p-10">
            <p class="font-bold text-4xl m-0 p-0">{{ about_data.title }}</p>
            <p class="font-normal text-2xl m-0 p-1">{{ host }}</p>
            <p class="mt-2 p-1">{{ about_data.description }}</p>
        </div>
        <div class="mx-2">
            <n-card embedded>
                <n-grid :cols="cols" :collapsed="true" :collapsed-rows="2">
                    <n-grid-item class="flex items-center justify-center">
                        <UserCard :name="about_data.admin_name" :uid="about_data.admin_id"
                            :avatar="about_data.admin_avatar" />
                    </n-grid-item>
                    <n-grid-item class="flex items-center justify-center">
                        <n-button round size="large" strong secondary tag="a" :href="about_data.contact">
                            {{ t('ui.pages.about.serverContactBtn') }}
                        </n-button>
                    </n-grid-item>
                </n-grid>
            </n-card>
        </div>
        <div class="mx-2">
            <n-card embedded>
                <n-grid :cols="cols * 2" :collapsed="true" :collapsed-rows="2">
                    <n-grid-item class="flex items-center justify-center">
                        <n-statistic label="联邦宇宙总用户数" tabular-nums>
                            <n-number-animation show-separator :from="0" :to="universe_user_count" />
                        </n-statistic>
                    </n-grid-item>
                    <n-grid-item class="flex items-center justify-center">
                        <n-statistic label="联邦宇宙30天活跃" tabular-nums>
                            <n-number-animation show-separator :from="0" :to="universe_user_count_30" />
                        </n-statistic>
                    </n-grid-item>
                    <n-grid-item class="flex items-center justify-center">
                        <n-statistic label="本服务器用户数" tabular-nums>
                            <n-number-animation show-separator :from="0" :to="about_data.users" />
                        </n-statistic>
                    </n-grid-item>
                    <n-grid-item class="flex items-center justify-center">
                        <n-statistic label="本服务器30天活跃" tabular-nums>
                            <n-number-animation show-separator :from="0" :to="about_data.users_of_30" />
                        </n-statistic>
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
                        <MarkdownViewer :content="about_data.about" />
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
                    <n-flex vertical>
                        <ServerRuleCard v-for="(rule, index) in about_data.rules" :key="index"
                            :rule_no="rule.order.toString()" :rule_content="rule.content"
                            :updated_at="rule.updated_at" />
                    </n-flex>
                </n-collapse-transition>
            </n-card>
        </div>
    </n-flex>

</template>