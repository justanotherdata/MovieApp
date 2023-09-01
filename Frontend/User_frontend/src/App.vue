<template>
  <Navbar :id="user_login_status"/>
  <RouterView :login="users"/>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import { mapState } from 'vuex'

export default{
  data() {
    return{
      token: null
    }
  },
  components: {
    Navbar
  },
  computed:{
      ...mapState(['user_login_status', 'users'])
      
  },
  mounted() {
    //console.log('onmounted from app page')
    this.$store.dispatch('get_user_login_status')
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
