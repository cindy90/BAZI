// frontend/src/router/modules/iching.js
import IChingCalculator from '../../views/iching/IChingCalculator.vue'

const ichingRoutes = [
  {
    path: '/iching',
    name: 'IChingIndex',
    redirect: '/iching/calculate'
  },
  {
    path: '/iching/calculate',
    name: 'IChingCalculator',
    component: IChingCalculator,
    meta: { 
      requiresAuth: true,
      title: '易经算卦'
    }
  }
]

export default ichingRoutes
