<template>
      <div class="div-des">
        <h1>All Bookings Page</h1>
    </div>
  <div v-if="login" class="container container_style">
    <h4>Displaying bookings for {{ login.user_name }}</h4>
    <div class = "movie-cards" >
      <Cards v-for="(show, index) in all_bookings" :key="index" :card_data="show" :page="allbookings" @cancel_bookingid="cancel"/>
    </div>
  </div>

  <div class="about" v-if="!login">
    <h1>User Booking Page</h1>
    <h2>You need to log in to access this page!</h2>
    <button @click="gohome" class="btn btn-primary">Go Home</button>
  </div>
    
</template>

<script>
import custom_cards from '@/components/MovieCard.vue'; 

export default{
  data(){
    return{
      allbookings:'All Bookings',
      id : 0
    }
  },
  components: {
    Cards : custom_cards
  },
  props: ['login'],
  computed: {
    all_bookings(){
      return this.$store.state.all_booking_data
    },
  },
  methods: {
    cancel(e){
      const param = e
      let user = localStorage.getItem('token')
      if (user) {
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", user)

        myHeaders.append("Content-Type","application/json")

        var raw = JSON.stringify({
        "booking_id": param,
        });

        const url = "http://127.0.0.1:5000/cancel_booking"
        
        console.log(url)
        
        
        var requestOptions = {
          method: 'POST',
          headers: myHeaders,
          body: raw
        };

        fetch(url, requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if (user_data.message === 'Success'){
              alert('Booking has been cancelled an email will be sent')
              this.id = this.id + 1
              //window.location.reload()
              this.$store.dispatch('get_all_bookings')
            }else{
              alert(user_data.details)
            }  
          })

          .catch(error => console.log('error', error));
      }
      else{
        console.log('You need to login to access this page!')
      }
    }
  },
  beforeMount() {
    let user_token = localStorage.getItem('token')
    if(user_token){
      this.$store.dispatch("get_all_bookings")
    }
    this.$store.dispatch('get_curr_page', 'All_Bookings') 
  }
}
</script>


<style scoped>
.movie-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

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