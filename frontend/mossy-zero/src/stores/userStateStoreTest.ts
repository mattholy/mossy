import { defineStore } from 'pinia'

interface UserState {
    token: string | null
    role: string
}

export const useUserStateStore = defineStore('user_test_state', {
    state: (): UserState => ({
        token: null,
        role: 'user'
    }),
    actions: {
        setToken(newToken: string): void {
            this.token = newToken;
        },
        clearToken(): void {
            this.token = null;
        }
    },
    getters: {
        isLoggedIn: (state) => state.token !== null,
        currentToken: (state) => state.token
    }
});