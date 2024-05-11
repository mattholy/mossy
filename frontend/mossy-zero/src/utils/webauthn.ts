import { startRegistration, startAuthentication } from '@simplewebauthn/browser'
import type { MessageReactive } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { useI18n } from 'vue-i18n'
import { callMossyApi } from './apiCall'
import { AuthenticationService } from '@/client/services.gen'
import { type PublicKeyCredentialCreationOptionsJSON, type PublicKeyCredentialRequestOptionsJSON } from '@simplewebauthn/types'

export function isWebAuthnSupported(): boolean {
    return window.PublicKeyCredential !== undefined &&
        typeof navigator.credentials.create === 'function' &&
        typeof navigator.credentials.get === 'function';
}

export async function webauthnRegister(uid: string): Promise<void> {
    const regOptionsResponse = await callMossyApi({
        endpoint: '/m1/auth/generate-registration-options',
        data: { username: uid }
    })
    const registrationData = await startRegistration(regOptionsResponse.payload);
    await callMossyApi({
        endpoint: '/m1/auth/verify-registration',
        data: {
            payload: registrationData,
            challenge: regOptionsResponse.payload.challenge
        }
    })
}
