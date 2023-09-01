<template>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">

  <div class="container-fluid">
    <router-link class="navbar-brand" to="/admin/home" v-if="user_role==='Admin' && user_login_status">Movie App</router-link>
    <router-link class="navbar-brand" to="/admin/login" v-if="user_role==='Admin' && !user_login_status">Movie App</router-link>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent" v-if="user_login_status">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item" v-if="user_login_status">
            <router-link class="nav-link" to='/admin/theatres'>Theatres</router-link>
        </li>
        <li class="nav-item" v-if="user_login_status">
         <router-link class="nav-link" to='/admin/movies'>Movies</router-link>
        </li>
        <li class="nav-item" v-if="user_login_status">
         <router-link class="nav-link" to='/admin/shows'>Shows</router-link>
        </li>
        <li class="nav-item" v-if="user_login_status">
         <router-link class="nav-link" to='/admin/bookings'>Bookings</router-link>
        </li>


        <li class="nav-item" v-if="!user_login_status && !user_role">
          <router-link class="nav-link" to='/pre_login'>Login</router-link>
        </li>
        <li class="nav-item" v-if="!user_login_status && user_role === 'Admin'">
          <router-link class="nav-link" to='/admin/login'>Login</router-link>
        </li>
        <li class="nav-item" v-if="user_login_status" >
            <router-link class="nav-link" to='/logout' @click="logoutadmin()">Logout</router-link>
        </li>
      </ul>
     </div> 
  </div>  
</nav>


</template>

<script>
import { mapState } from 'vuex'

export default{
    data(){
        return{
        }
    },
    props: ['id'],
    computed:{
        ...mapState(['user_login_status']),
    user_role(){
      return this.$store.state.role
    }

    },
    mounted(){
    },
    methods: {
        
        logoutadmin() {
            let user = localStorage.getItem('token')
            if (user){
            var myHeaders = new Headers();
            myHeaders.append("x-access-token", user);

            var requestOptions = {
            method: 'GET',
            headers: myHeaders
            };

            fetch("http://127.0.0.1:5000/logout_admin", requestOptions)
            .then(response => response.json())
            .then(result => console.log(result))
            .catch(error => console.log('error', error));

            localStorage.removeItem('token')
            this.$store.dispatch('get_user_login_status')
            alert('You have been logged out')
            //window.location.reload()
            this.$router.push({path:'/admin/login'})
            } 
            
            else{
                alert('You are already logged out!')
                this.$router.push({path:'/admin/login'})
            }
            
        }
    }
  }
</script>

<style></style>