// frontend/src/router/modules/auth.js
import Login from '../../views/auth/Login.vue';
import Register from '../../views/auth/Register.vue';

const authRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false },
  },
];

export default authRoutes;