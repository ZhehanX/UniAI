import { createRouter, createWebHistory } from 'vue-router';
import { getUserRole } from '@/utils/auth.js';
import HomeView from '@/views/HomeView.vue';
import AppDetail from '@/views/AppDetails.vue';
import SubmitProject from '@/views/SubmitProject.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/app/:id',
    name: 'AppDetail',
    component: AppDetail,
    props: true // Pass route params as props
  },
  {
    path: '/submit-project',
    name: 'SubmitProject',
    component: SubmitProject
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: () => import('../views/SignUp.vue')
  },
  {
    path:'/graphs',
    name: 'Graphs',
    component: () => import('../views/Graphs.vue')
  },
  {
    path: '/admin/review',
    name: 'AdminReview',
    component: () => import('@/views/AdminReview.vue'),
    meta: { requiresAuth: true },
    beforeEnter: (to, from, next) => {
      const userRole = getUserRole();
      if (userRole === 'admin') {
        next();
      } else {
        alert('Admin access required');
        next('/');
      }
    }
  },
  {
    path: '/my-projects',
    name: 'UserUseProjects',
    component: () => import('@/views/UserProjects.vue'),
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;