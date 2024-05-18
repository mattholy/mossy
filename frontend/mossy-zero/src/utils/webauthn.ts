import { startRegistration, startAuthentication } from '@simplewebauthn/browser'
import { callMossyApi, MossyApiError } from './apiCall'
import pinia from '@/stores';
import { useUserStateStore } from '@/stores/userStateStore';
import type { PublicKeyCredentialCreationOptionsJSON, PublicKeyCredentialRequestOptionsJSON, RegistrationResponseJSON, AuthenticationResponseJSON } from '@simplewebauthn/types'

export async function webauthnRegister(uid: string): Promise<void> {
    let regOptions: PublicKeyCredentialCreationOptionsJSON
    let registrationData: RegistrationResponseJSON
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
        registrationData = await startRegistration(regOptions);
    } catch (error: any) {
        throw new Error(error.name as string)
    }

    try {
        await callMossyApi({
            endpoint: '/api/m1/auth/verify-registration',
            data: {
                payload: registrationData,
                challenge: regOptions.challenge
            }
        })
    } catch (error) {
        if (error instanceof MossyApiError) {
            throw new Error(error.detail)
        }
        throw error
    }

}

export async function webauthnAuthentication(): Promise<string> {
    let authOptions: PublicKeyCredentialRequestOptionsJSON
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
        authData = await startAuthentication(authOptions);
    } catch (error: unknown) {
        if (isErrorWithMessage(error)) {
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
                challenge: authOptions.challenge
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
    return authResp.token
}

function isErrorWithMessage(error: any): error is { name: string } {
    return error && typeof error.name === 'string';
}