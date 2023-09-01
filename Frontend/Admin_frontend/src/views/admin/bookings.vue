<template>
    <div class="div-des">
        <h1>Bookings Page</h1>
    </div>
    <div class="container container_style">
        <h3 v-if="login">All Bookings for user_id: {{ login.user_id }}</h3>
        <div class="movie-cards container" v-if="booking_data">
            <Cards :page="page" v-for="(data, index) in booking_data" :key="index" :card_data="data" @cancel_booking_id="cancel_booking"/>
        </div>
        <div class = 'container' v-if="!booking_data">
            <h1>There are no active bookings for this user</h1>
            
            <button class="btn btn-primary col-9" @click="gotomovies">Movies</button>
        </div>
    </div>
   
</template>

<script>
import cards from '@/components/cards.vue'

export default{
    data(){
        return{
            page: 'booking'
        }
    },
    props: ['login'],
    components:{Cards: cards},
    computed:{
        booking_data(){
            return this.$store.state.booking_data
        },
        show_id(){
            return this.$route.params.Show_Id;
        }
    },
    methods:{
        gotomovies(){
            this.$router.push({path: '/admin/movies'})
        },
        //Event Based Method
        cancel_booking(e){
            let url = "http://127.0.0.1:5000/admin/cancel_booking/"
            let param = e
            let final_url = url.concat(param)
            //console.log(final_url)
            let user_token = localStorage.getItem('token')
            if(user_token){
                    var myHeaders = new Headers();
                    myHeaders.append("x-access-token", user_token);
                    myHeaders.append("Content-Type", "application/json");

                    var requestOptions = {
                    method: 'GET',
                    headers: myHeaders,
                    };

                    fetch(final_url, requestOptions)
                    .then(response => response.json())
                    .then(result => {
                       const data = result;
                       if (data.message === 'Success') {
                        alert('Ticket Cancelled!')
                        window.location.reload()
                       }else{
                        alert(data.details)
                       }
                    })
                    .catch(error => console.log('error', error));
                }
                else{
                    console.log('You are not logged in!')
                }
        },
        
    },
    beforeMount(){
        this.$store.dispatch('get_booking_data')
    }
}
</script>

<style scoped>
.movie-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.container_style{
    padding-top: 20px;
    align-items: start;
}
.div-des{
    background-color: rgb(219, 219, 216);
    align-items: start;
    padding: 10px;
    
}
</style>