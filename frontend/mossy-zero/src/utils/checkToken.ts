import { callMossyApi, MossyApiError } from "./apiCall";
import { notyf } from "./notyf";
import i18n from '@/i18n';
import pinia from '@/stores';
import { useUserStateStore } from '@/stores/userStateStore';

const { t } = i18n.global;

export async function checkToken(token: string): Promise<boolean> {
    return await callMossyApi({
        endpoint: '/api/m1/auth/verify-jwt',
        data: { token }
    })
        .then((res) => {
            return true;
        })
        .catch((error) => {
            if (error instanceof MossyApiError) {
                notyf.error(t(`api.statusmsg.${error.detail}.notification`));
            }
            const userStateStore = useUserStateStore(pinia);
            userStateStore.clearToken();
            return false;
        });
}
