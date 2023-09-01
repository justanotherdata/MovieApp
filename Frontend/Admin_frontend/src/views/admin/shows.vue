<template>
    <div class="div-des">
        <h1>Shows Page</h1>
    </div>
    <div class="container container_style">
        <h3 v-if="login">All Movies for user_id: {{ login.user_id }}</h3>
        <button class="btn btn-dark col-6 btn_style" @click="gotoaddshow"><h5>Add New Show</h5></button>
        <div class="movie-cards container" v-if="shows_data" :id="shows_data">
            <Cards :page="page" v-for="(data, index) in shows_data" :key="index" :card_data="data" @disable_show_id="disable_show" @get_bookings_show_id="get_show_booking" @enable_show_id="enable_show" @delete_show_id="delete_show"/>
        </div>
        <div class="container" v-if="!shows_data">
            <h1>No Shows have been created By this User</h1>
            <h2>Go Back to Movies Page And Create Some Movies From There!</h2>
            <button class="btn btn-primary col-9" @click="gotomovies">Movies</button>
        </div>
    </div>
</template>

<script>
import cards from '@/components/cards.vue'

export default{
    data(){
        return{
            page: 'shows'  
        }
    },
    props: ['login'],
    components: {Cards: cards},
    computed: {
        shows_data(){
            return this.$store.state.shows_data
        }
    }, 
    methods:{
        gotomovies(){
        this.$router.push({path: '/admin/movies'})
        },
        gotoaddshow(){
            this.$router.push({path: '/admin/add_show'})
        },
      //Event based methods
      disable_show(e){

        let url = "http://127.0.0.1:5000/admin/disable_show/"
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
                        alert('Show Disabled!')
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
      get_show_booking(e){
        const path = '/admin/bookings/'
        const param = e
        const final_path = path.concat(param)
        this.$router.push({path: final_path})

      },
      enable_show(e){
        let url = "http://127.0.0.1:5000/admin/enable_show/"
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
                        alert('Show Enabled!')
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
      delete_show(e){
        let url = "http://127.0.0.1:5000/admin/delete_show/"
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
                        alert('Show Deleted!')
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
      }
    },
    beforeMount(){
        this.$store.dispatch('get_shows_data')
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