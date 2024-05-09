import { defineStore } from 'pinia';

interface PermissionsState {
    permissions: string[];
}

export const usePermissionsStore = defineStore({
    id: 'permissions',
    state: (): PermissionsState => ({
        permissions: []
    }),
    getters: {
        hasPermission: (state) => (permission: string) => state.permissions.includes(permission)
    },
    actions: {
        setPermissions(permissions: string[]) {
            this.permissions = permissions;
        }
    },
    persist: true
});
