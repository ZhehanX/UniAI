import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import AppDetail from '@/views/AppDetails.vue';
import SubmitCase from '@/views/SubmitCase.vue';

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
    path: '/submit-case',
    name: 'SubmitCase',
    component: SubmitCase
}
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;