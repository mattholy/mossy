import { callMossyApi, MossyApiError } from "./apiCall";
import { notyf } from "./notyf";
import i18n from '@/i18n';
import pinia from '@/pinia';
import { useAuthStore } from '@/stores/authStore';

const { t } = i18n.global;
const authStore = useAuthStore(pinia);

export async function checkToken(token: string): Promise<boolean> {
    console.log('checkToken');
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
            authStore.clearToken();
            return false;
        });
}
