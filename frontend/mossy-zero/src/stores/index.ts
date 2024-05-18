import { createPinia } from 'pinia'
import { createPersistedState } from 'pinia-plugin-persistedstate'

const pinia = createPinia()

pinia.use(
    createPersistedState({
        auto: true,
        storage: localStorage,
        key: id => `__persisted__${id}`,
    })
)

export default pinia