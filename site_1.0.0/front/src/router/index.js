import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Admin from '../views/Administration.vue'
import Hospital from '../views/Hospital.vue'
import MES from '../views/MES.vue'
import Login from '../views/Login.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/administration',
    name: 'Admin',
    component: Admin
  },
  {
    path: '/hospital',
    name: 'Hospital',
    component: Hospital
  },
  {
    path: '/mes',
    name: 'MES',
    component: MES
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
