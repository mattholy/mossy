import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';
import VueDevTools from 'vite-plugin-vue-devtools';
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite';
import { visualizer } from 'rollup-plugin-visualizer';
import path from 'path';
import { mergeConfig } from 'vite';
import vitestConfig from './vitest.config';

export default defineConfig(({ mode }) => {
  const isDev = mode === 'development';

  const baseConfig = {
    plugins: [
      vue(),
      vueJsx(),
      VueDevTools(),
      VueI18nPlugin({}),
      // Conditionally add the visualizer plugin
      ...(isDev ? [visualizer({ open: true })] : [])
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    build: {
      target: 'esnext',
      outDir: isDev ? path.resolve(__dirname, '../../backend/static') : 'dist',
      rollupOptions: {
        output: {
          manualChunks(id: string) {
            if (id.includes('node_modules/highlight.js')) {
              return 'highlight.js';
            }
            if (id.includes('node_modules/naive-ui')) {
              return 'naive-ui';
            }
            if (id.includes('node_modules')) {
              return 'vendor';
            }
            if (id.includes('src/components')) {
              return 'components';
            }
          },
        },
      },
    }
  };

  // Merge the base Vite config with Vitest config
  return mergeConfig(baseConfig, vitestConfig);
});
