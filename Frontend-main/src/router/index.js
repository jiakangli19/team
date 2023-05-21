import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/components/HomePage.vue'
import TwitterAll from '@/components/TwitterAll.vue'
import TwitterJob from '@/components/TwitterJob.vue'
import SudoPage from '@/components/SudoPage.vue'

const routes = [
        {
            path: '/',
            name: 'HomePage',
            component: HomePage
        },
        {
            path: '/view1',
            name: 'TwitterAll',
            component: TwitterAll
        },
        {
            path: '/view2',
            name: 'TwitterJob',
            component: TwitterJob
        },
        {
            path: '/view3',
            name: 'SudoPage',
            component: SudoPage
        }
    ]
const router = createRouter({
    history: createWebHistory(),
    routes
})
export default router