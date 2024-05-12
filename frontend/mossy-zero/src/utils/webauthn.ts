import { startRegistration, startAuthentication } from '@simplewebauthn/browser'
import type { MessageReactive } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { useI18n } from 'vue-i18n'
import { callMossyApi } from './apiCall'
import { AuthenticationService } from '@/client/services.gen'
import { type PublicKeyCredentialCreationOptionsJSON, type PublicKeyCredentialRequestOptionsJSON } from '@simplewebauthn/types'
import { useAuthStore } from '@/stores/AuthStore'

const authStore = useAuthStore()

export async function webauthnRegister(uid: string): Promise<void> {
    const regOptions = await callMossyApi({
        endpoint: '/m1/auth/generate-registration-options',
        data: { username: uid }
    })
    const registrationData = await startRegistration(regOptions);
    await callMossyApi({
        endpoint: '/m1/auth/verify-registration',
        data: {
            payload: registrationData,
            challenge: regOptions.challenge
        }
    })
}

export async function webauthnAuthncation(): Promise<void> {
    const authOptions = await callMossyApi({
        endpoint: '/m1/auth/generate-authentication-options'
    })
    const authData = await startAuthentication(authOptions)
    const authResp = await callMossyApi({
        endpoint: '/m1/auth/verify-authentication',
        data: {
            payload: authData,
            challenge: authOptions.challenge
        }
    })
    authStore.setToken(authResp.token)
}