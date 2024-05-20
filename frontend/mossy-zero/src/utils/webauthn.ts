import { startRegistration, startAuthentication } from '@simplewebauthn/browser'
import { callMossyApi, MossyApiError } from './apiCall'
import pinia from '@/stores';
import { useUserStateStore } from '@/stores/userStateStore';
import type { PublicKeyCredentialCreationOptionsJSON, PublicKeyCredentialRequestOptionsJSON, RegistrationResponseJSON, AuthenticationResponseJSON } from '@simplewebauthn/types'
import type { RouteLocationNormalizedLoaded } from 'vue-router';

interface webauthnRegisterResponse {
    mossy_id: string,
    webauthn: PublicKeyCredentialCreationOptionsJSON
}

interface webauthnAuthncationResponse {
    mossy_id: string,
    webauthn: PublicKeyCredentialRequestOptionsJSON
}

export async function webauthnRegister(uid: string, route?: RouteLocationNormalizedLoaded): Promise<String> {
    let regOptions: webauthnRegisterResponse
    let registrationData: RegistrationResponseJSON
    let recovery_key: String
    try {
        regOptions = await callMossyApi({
            endpoint: '/api/m1/auth/generate-registration-options',
            data: { username: uid }
        })
    } catch (error) {
        if (error instanceof MossyApiError) {
            throw new Error(error.detail)
        }
        throw error
    }

    try {
        registrationData = await startRegistration(regOptions.webauthn);
    } catch (error: any) {
        console.log(error)
        if (isErrorWithMessage(error)) {
            if (error.message.startsWith('WebAuthn is not supported')) {
                throw new Error('WebauthnNotReady');
            }
            throw new Error(error.name);
        } else {
            throw new Error('UnknownError');
        }
    }

    try {
        recovery_key = await callMossyApi({
            endpoint: '/api/m1/auth/verify-registration',
            data: {
                payload: registrationData,
                mossy_id: regOptions.mossy_id,
                register_from: (route && route.query.client_name) ? route.query.client_name.toString() : 'MossyWebApp'
            }
        }).then((res) => {
            if (res.recovery_key) {
                return res.recovery_key
            } else {
                return ''
            }
        })
    } catch (error) {
        if (error instanceof MossyApiError) {
            throw new Error(error.detail)
        }
        throw error
    }
    return recovery_key
}

export async function webauthnAuthentication(): Promise<any> {
    let authOptions: webauthnAuthncationResponse
    let authData: AuthenticationResponseJSON
    let authResp: any
    try {
        authOptions = await callMossyApi({
            endpoint: '/api/m1/auth/generate-authentication-options'
        })
    } catch (error) {
        if (error instanceof MossyApiError) {
            throw new Error(error.detail)
        }
        throw error
    }

    try {
        authData = await startAuthentication(authOptions.webauthn);
    } catch (error: unknown) {
        if (isErrorWithMessage(error)) {
            if (error.message.startsWith('WebAuthn is not supported')) {
                throw new Error('WebauthnNotReady');
            }
            throw new Error(error.name);
        } else {
            throw new Error('UnknownError');
        }
    }

    try {
        authResp = await callMossyApi({
            endpoint: '/api/m1/auth/verify-authentication',
            data: {
                payload: authData,
                mossy_id: authOptions.mossy_id
            }
        });
    } catch (error) {
        if (error instanceof MossyApiError) {
            throw new Error(error.detail)
        }
        throw error
    }
    const userStateStore = useUserStateStore(pinia);
    userStateStore.setToken(authResp.token)
    return authResp
}

function isErrorWithMessage(error: any): error is { name: string, message: string } {
    return error && typeof error.name === 'string' && typeof error.message === 'string'
}