<template>
  <div class="div-des">
        <h1>Theatre Movies Page</h1>
    </div>
    <div class="container_style">
      <h3>Showing all movies for The_Id: {{ the_id }}</h3>
    </div>
    <Cards :page= "theatre" :card_data="theatres" @trigger_get_shows="getshowdata"/>
</template>

<script>
import custom_cards from '@/components/Cards copy.vue'; 

export default{
  data(){
    return{
      theatre:'theatres'
    }
  },
  components: {
    Cards: custom_cards
  },
  props:['login'],
  computed: {
    theatres(){
      return this.$store.state.card_data
    },
    the_id(){
      return this.$route.params.The_Id;
    },
    city(){
      return this.$store.state.user_city
    }
  },
  methods: {
    getshowdata(e){
    const path_ = '/shows/'  
    const param = e
    const final_path = path_.concat(param)
    
    this.$router.push({path: final_path})},

  },
  beforeMount() {
    const url = 'http://127.0.0.1:5000/user/get_movie/'
    const the = this.the_id
    const city = this.city
    const pre_url_1 = url.concat(the)
    const pre_url_2 = pre_url_1.concat('/')
    const final_url = pre_url_2.concat(city)
    
    this.$store.dispatch("get_theatre_movies", final_url)
    
    this.$store.dispatch('get_curr_page', null)
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
