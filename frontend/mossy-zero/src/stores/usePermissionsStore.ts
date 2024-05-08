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
        // Getter来检查用户是否具有特定权限
        hasPermission: (state) => (permission: string) => state.permissions.includes(permission)
    },
    actions: {
        // Action来设置用户权限
        setPermissions(permissions: string[]) {
            this.permissions = permissions;
        }
    },
    persist: true
});
