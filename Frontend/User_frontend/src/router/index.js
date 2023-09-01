import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store';

//importing for users

import HomeView from '../views/user/HomeView.vue'
import AboutView from '../views/user/AboutView.vue'
import All_Bookings from '../views/user/All_Bookings.vue'
import Booking_Page from '../views/user/Booking_Page.vue'

import Login from '../views/user/Login.vue'
import Signup from '../views/user/Signup.vue'

import Search from '../views/user/Search.vue'
import Shows from '../views/user/Shows.vue'
import Theatres from '../views/user/Theatres.vue'
import PageNotFound from '../views/404.vue'



const router = new createRouter({
  //base: 'http://localhost:8080/',
  history: createWebHistory(process.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      props:true
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
      beforeEnter: (to, from, next) => {
        if (!store.state.users) {
          next({ path: '/'})
        } else {
          next();
        }
      },
      props:true
    },
    {
      path: '/all_bookings',
      name: 'all_bookings',
      component: All_Bookings,
      
      props:true
    },
    {
      path: '/bookings_page/:show_id',
      name: 'bookings_page',
      component: Booking_Page,
      //props: true
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      beforeEnter: (to, from, next) => {
        if (store.state.users) {
          next({ path: '/'})
        } else {
          next();
        }
      },
      props:true
    },
    {
      path: '/search',
      name: 'search',
      component: Search,
      props:true
    },
    {
      path: '/shows/:Mov_Id',
      name: 'shows_movies',
      component: Shows,
      //props: true
    },
    {
      path: '/logout',
      redirect: '/'
    },
    {
      path: '/Theatres/:The_Id',
      name: 'Theatre_movies',
      component: Theatres,
      //props: true
    },
    {
      path: '/theatres',
      name: 'theatres',
      component: Theatres,
      props:true
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup,
      beforeEnter: (to, from, next) => {
        if (store.state.user_login_status) {
          next({ name: 'home'})
        } else {
          next();
        }
      }
    },
    {
      path: '/:catchAll(.*)',
      name: 'pageNotFound',
      component: PageNotFound
    }
  ]
});


export default router
