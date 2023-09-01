<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light" v-if="!user_role || user_role === 'User'">
  <div class="container-fluid">
    <router-link class="navbar-brand" to="/">Movie App</router-link>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item" v-if="user_login_status">
            <router-link class="nav-link" to='/about'>Profile</router-link>
        </li>
        <li class="nav-item" v-if="user_login_status">
         <router-link class="nav-link" to='/all_bookings'>All Bookings</router-link>
          
        </li>
        <li class="nav-item" v-if="!user_login_status && !user_role">
          <router-link class="nav-link" to='/login'>Login</router-link>
        </li>
        <li class="nav-item" v-if="!user_login_status && user_role === 'User'">
          <router-link class="nav-link" to='/login'>Login</router-link>
        </li>
        <li class="nav-item" v-if="!user_login_status">
            <router-link class="nav-link" to='/signup'>Signup</router-link>
        </li>
        <li class="nav-item" v-if="user_login_status" >
            <router-link class="nav-link" to='/logout' @click="logoutuser()">Logout</router-link>
        </li>
      </ul>
      
      <div class="nav-item dropdown" :id="current_page">
          <span class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            <a v-if="!selected_city">Bangalore</a>
            <a v-if="selected_city">{{ selected_city }}</a>
          </span>
          
          <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
            <li v-for="city in cities" :id="city">
            <a  class="dropdown-item dropdown" value="movie" @click="reload_page(city)">{{ city }}</a>
            </li>
          </ul>
        </div> 
      <form class="d-flex">
        <input class="form-control me-2" type="search" placeholder="Search Movie" aria-label="Search" v-model="search">
        <button class="btn btn-outline-success" type="button" @click="search_movie">Search</button>
      </form>
    </div>
  </div>
</nav>




</template>

<script>
import { mapState } from 'vuex'
import { mapGetters, mapActions } from 'vuex'

export default{
    data(){
        return{
            search: null,
            cities: null,
            selected_city: null
        }
    },
    props: ['id'],
    computed:{
        ...mapState(['user_login_status']),
        user_city(){
      return this.$store.state.user_city
    },
    current_page(){
      return this.$store.state.curr_page
    },
    user_role(){
      return this.$store.state.role
    }

    },
    mounted(){
        const url = "http://127.0.0.1:5000/all_cities"
       
        var requestOptions = {
          method: 'GET',
        };

        fetch(url, requestOptions)
          .then(response => response.json())
          .then(result => {
            this.cities = result;
            
          })

          .catch(error => console.log('error', error));
    },
    methods: {
        
        logoutuser() {
            console.log("User Logged Out")
            
            let user = localStorage.getItem('token')
            if (user){
            var myHeaders = new Headers();
            myHeaders.append("x-access-token", user);

            var requestOptions = {
            method: 'GET',
            headers: myHeaders
            };

            fetch("http://127.0.0.1:5000/logout_user", requestOptions)
            .then(response => response.json())
            .then(result => console.log(result))
            .catch(error => console.log('error', error));

            localStorage.removeItem('token')
            this.$store.dispatch('get_user_login_status')
            
            this.$router.push({path:'/login'})
            } else{
                alert('You are already logged out!')
              
                this.$router.push({path:'/login'})
            }
            

            
            
        },

        search_movie() {
            if(this.search){
                const param = this.search
                const param2 = 'movie'
                const param3 = this.selected_city
                this.$store.dispatch('get_search_data', {'value1': param, 'value2': param2, 'value3': param3})
                this.$router.push({path:'/search'})
            }else{
                alert('Button click working properly')
            }
        },

        reload_page(city){
          
          const param = city
          
          if(this.current_page==='Home'){
            this.selected_city = city 
            this.$store.dispatch('get_user_city', param)
            this.$store.dispatch('get_movies', param)
          }else{
            this.selected_city = city 
            this.$store.dispatch('get_user_city', param)
            this.$router.push({path:'/'})
            
            
          }

        },

        closeDropdown() {
      
          const dropdownMenu = document.querySelector('.dropdown-menu');
          if (dropdownMenu) {
        dropdownMenu.classList.remove('show');
      } 
    }

    }
  }
</script>

<style></style>