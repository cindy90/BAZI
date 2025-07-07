// frontend/src/router/modules/user.js
import BaziCalculator from '../../views/bazi/BaziCalculator.vue';
import BaziResult from '../../views/bazi/BaziResult.vue';
import IChingCalculator from '../../views/iching/IChingCalculator.vue';

const userRoutes = [
  {
    path: '/bazi/calculate',
    name: 'BaziCalculator', // 路由名称，用于 router.push({ name: 'BaziCalculator' })
    component: BaziCalculator,
    meta: { requiresAuth: true }, // 需要登录才能访问
  },
  {
    path: '/bazi/result',
    name: 'BaziResult',
    component: BaziResult,
    meta: { requiresAuth: true }, // 需要登录才能访问
  },
  {
    path: '/iching/calculate',
    name: 'IChingCalculator',
    component: IChingCalculator,
    meta: { 
      requiresAuth: true,
      title: '易经算卦'
    }
  },
];

export default userRoutes;