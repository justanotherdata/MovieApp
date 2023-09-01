<template>
    <div class="div-des">
        <h1>Custom Bookings Page</h1>
    </div>
    <div class="container container_style">
        <h3 v-if="show_id">All Bookings for Show_id: {{ show_id }}</h3>
        <div class="movie-cards container" v-if="booking_data" :id="booking_data">
            <Cards :page="page" v-for="(data, index) in booking_data" :key="index" :card_data="data" @cancel_booking_id="cancel_booking"/>
            
        </div>
        <div class="container container_style" v-if="!booking_data" :id="booking_data">
            <h3>No Bookings for this show</h3>
            <button class="btn btn-dark col-6 btn_style" @click="gotoshow"><h5>Go To Show</h5></button>
        </div>
    </div>
   
</template>

<script>
import cards from '@/components/cards.vue'

export default{
    data(){
        return{
            page: 'custom_booking'
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
        gotoshow(){
            this.$router.push({path: '/admin/shows'})
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
        this.$store.dispatch('get_custom_booking_data', this.show_id)
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
.btn_style{
    padding: 5px;
    padding-top: 10px;
    margin: 5px
}
</style>