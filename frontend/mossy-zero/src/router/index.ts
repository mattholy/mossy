import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router';
import { checkToken } from '@/utils/checkToken';
import pinia from '@/stores';
import { useUserStateStore } from '@/stores/userStateStore';

type ExtendedRoute = RouteRecordRaw & {
  children?: ExtendedRoute[];
};
const viewModules = import.meta.glob('../views/**/*.vue');
// const baseUrl = import.meta.env.VITE_BASE_URL || '';

function pathToRoute(path: string): ExtendedRoute {
  const segments = path.replace(/^.*[\\\\/]views[\\\\/](.*)\.vue$/, '$1').split('/');
  const name = segments[segments.length - 1];
  const routePath = segments
    .map(s => s.replace('View', ''))
    .map(s => s.replace(/[A-Z]/g, match => '-' + match.toLowerCase()))
    .map(s => s.replace('.', '/:'))
    .map(s => s.toLowerCase()).join('/')

  return {
    path: `/${routePath}`,
    name: 'view-' + name.replace(/View$/, '').replace(/[A-Z]/g, match => '-' + match.toLowerCase()),
    component: viewModules[path],
    children: []
  };
}

async function setupRoutes(): Promise<ExtendedRoute[]> {
  const routesMap: { [key: string]: ExtendedRoute } = {};

  for (const path in viewModules) {
    const route = pathToRoute(path);
    routesMap[route.path] = route;
  }

  Object.values(routesMap).forEach(route => {
    const segments = route.path.split('/');
    let currentPath = '';
    for (let i = 1; i < segments.length - 1; i++) {
      currentPath += '/' + segments[i]
      if (routesMap[currentPath]) {
        if (!routesMap[currentPath].children) {
          routesMap[currentPath].children = [];
        }
        routesMap[currentPath].children!.push(route);
      }
    }
  });

  const nestedRoutes = Object.values(routesMap)

  nestedRoutes.push({
    path: '/',
    redirect: '/home'
  });
  nestedRoutes.push({
    path: '/:catchAll(.*)',
    component: () => import('@/views/error/404View.vue')
  });
  return nestedRoutes;
}

const routes = await setupRoutes()

const router = createRouter({
  history: createWebHashHistory(import.meta.env.VITE_BASE_URL),
  routes,
});

router.beforeEach(async (to) => {
  const userStateStore = useUserStateStore(pinia);

  if (
    to.path.startsWith('/home') ||
    to.path.startsWith('/notifications') ||
    to.path.startsWith('/conversations') ||
    to.path.startsWith('/collections') ||
    to.path.startsWith('/settings')

  ) {
    if (!userStateStore.isLoggedIn) {
      return '/about'
    } else {
      const isValid = await checkToken(userStateStore.currentToken as string);
      if (!isValid) {
        return '/about'
      } else {
        return true
      }
    }
  }
});

export default router;
