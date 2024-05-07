
import { defineStore } from 'pinia';

interface AuthState {
  token: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: null
  }),
  actions: {
    setToken(newToken: string) {
      this.token = newToken;
    },
    clearToken() {
      this.token = null;
    }
  },
  getters: {
    isLoggedIn: (state) => state.token !== null
  },
  persist: true
});
