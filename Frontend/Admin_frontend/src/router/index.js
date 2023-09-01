import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store';


import PageNotFound from '../views/404.vue'

//import for admin

import Admin_home from '../views/admin/home.vue'
import Admin_login from '../views/admin/login.vue'
import Admin_movies from '../views/admin/movies.vue'
import Admin_theatres from '../views/admin/theatres.vue'
import Admin_shows from '../views/admin/shows.vue'
import Admin_thankyou from '../views/admin/thankyou.vue'
import Admin_booking from '../views/admin/bookings.vue'
import Admin_add_theatre from '../views/admin/add_theatre.vue'
import Admin_add_movie from '../views/admin/add_movie.vue'
import Admin_add_shows from '../views/admin/add_shows.vue'
import Admin_custom_booking from '../views/admin/custom_booking.vue'
import Admin_custom_movie from '../views/admin/custom_movie.vue'
import Admin_custom_show from '../views/admin/custom_shows.vue'





const router = new createRouter({
  //base: 'http://localhost:8080/',
  history: createWebHistory(process.env.BASE_URL),
  routes: [
    //admin routes
    {
      path: '/admin/home',
      name: 'admin_home',
      component: Admin_home,
      props:true
    },
    {
      path: '/admin/login',
      name: 'admin_login',
      component: Admin_login,
      props:true
    },
    {
      path: '/admin/theatres',
      name: 'admin_theatres',
      component: Admin_theatres,
      props:true
    },
    {
      path: '/admin/add_theatre',
      name: 'admin_add_theatre',
      component: Admin_add_theatre,
      props:true
    },
    {
      path: '/admin/movies',
      name: 'admin_movies',
      component: Admin_movies,
      props:true
    },
    {
      path: '/admin/movies/:theatre_id',
      name: 'admin_movies_theatre',
      component: Admin_custom_movie,
      //props:true
    },
    {
      path: '/admin/add_movie',
      name: 'admin_add_movie',
      component: Admin_add_movie,
      props:true
    },
    {
      path: '/admin/shows',
      name: 'admin_shows',
      component: Admin_shows,
      props:true
    },
    {
      path: '/admin/shows/:movie_id',
      name: 'admin_shows_movies',
      component: Admin_custom_show,
      //props:true
    },
    {
      path: '/admin/add_theatre',
      name: 'admin_add_theatre',
      component: Admin_add_theatre,
      props:true
    },{
      path: '/admin/add_show',
      name: 'admin_add_show',
      component: Admin_add_shows,
      props:true
    },
    {
      path: '/admin/thankyou',
      name: 'admin_thankyou',
      component: Admin_thankyou,
      props:true
    },
    {
      path: '/admin/bookings',
      name: 'admin_bookings',
      component: Admin_booking,
      props:true
    },
    {
      path: '/admin/bookings/:Show_Id',
      name: 'admin_booking_show',
      component: Admin_custom_booking,
      //props:true
    },
    {
      path: '/:catchAll(.*)',
      name: 'pageNotFound',
      component: PageNotFound
    }
  ]
});


export default router
