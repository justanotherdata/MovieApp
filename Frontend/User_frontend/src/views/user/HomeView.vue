<template>
  <div class="div-des">
        <h1>Home Page</h1>
    </div>
  <div class="container container_style" v-if="user" :key="user.user_name">
     <h4>
        Hello, {{ user['user_name'] }}!
     </h4>
    <h5>
      Displaying results from {{ user_city }}  
     </h5> 
  </div>
  
  <div class="container container_style" v-else>
    <h3>
      Hello, user!
      <h3>
      Displaying results from {{ user_city }}
     </h3>
    </h3>
  </div>

  <Cards :card_data="movies" :page="home" @trigger_get_shows="getshowdata"/>
</template>

<script>
import custom_cards from '@/components/Cards copy.vue';
import { mapGetters } from 'vuex';
export default{
  data(){
    return{
      home:'home',
      selected_city: 'Bangalore'
    }
  },
  props: ['login'], 
  components: {
    Cards: custom_cards
  },
  computed:{
    movies(){
      return this.$store.state.card_data
    },
    user(){
      return this.$store.state.users
    },
    user_city(){
      return this.$store.state.user_city
    }
  },
  methods: {
    getshowdata(e){
    const path_ = '/shows/'  
    const param = e
    const final_path = path_.concat(param)
    
    this.$router.push({path: final_path})
  }
  },
  created() {
    
    if (this.user_city){
      this.$store.dispatch("get_movies", this.user_city)
    }
    else{
      this.$store.dispatch("get_movies", 'Bangalore')
    }
    
  },
  mounted() {
    this.$store.dispatch('get_curr_page', 'Home')
  }
}
</script>


<style scoped>
.div-des{
    background-color: rgb(182, 176, 171);
    align-items: start;
    padding: 10px;  
}

.container_style{
    padding-top: 20px;
    align-items: start;
}
</style>

