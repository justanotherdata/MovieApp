<template>
    <div class="div-des">
        <h1>Shows Page</h1>
    </div>
  <div class="container_style">
    <Cards :card_data="show" :page="Show" @trigger_show_detail="getbookingdata"/>
  </div>
        
</template>

<script>
import custom_cards from '@/components/Cards copy.vue';

export default{
  data(){
    return{
      Show:'shows'
    }
  },
  props: ['login'],
  components: {
    Cards: custom_cards
  },
  computed:{
    show(){
      return this.$store.state.card_data
    },
    mov_id(){
      return this.$route.params.Mov_Id;
    },
    city(){
      return this.$store.state.user_city
    }
  },
  methods: {
    getbookingdata(e){
      if(this.login){

        const path_ = '/bookings_page/'  
        const param = e
        const final_path = path_.concat(param)
        this.$router.push({path: final_path})
        console.log('We will go to the booking page of show_id')
        console.log('On booking page we will fetch the details of that particular show')
        console.log(e)

      }else{
        alert('You Need To Login To Continue!')
        this.$router.push({path:'/login'})
      }
      
    }
  },
  beforeMount() {
    const url = 'http://127.0.0.1:5000/user/get_show/'
    const the = this.mov_id
    const city = this.city
    const pre_url_1 = url.concat(the)
    const pre_url_2 = pre_url_1.concat('/')
    const final_url = pre_url_2.concat(city)
    //console.log(final_url)
    this.$store.dispatch('get_curr_page', 'shows')
    this.$store.dispatch("get_shows", final_url)

    
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