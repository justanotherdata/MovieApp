<template>
    <div class="div-des">
        <h1>Theatres Page</h1>
    </div>
    <div class="container container_style">
        <h3 v-if="login">All Theatres for user_id: {{ login.user_id }}</h3>
        <button class="btn btn-dark col-6 btn_style" @click="gotoaddtheatre"><h5>Add New Theatre</h5></button>
        <div class="movie-cards container" v-if="theatres_data">
            <Cards :page="page" v-for="(data, index) in theatres_data" :key="index" :card_data="data"  @disable_theatre_id="disable_theatre" @get_movies_the_id="get_movies" @enable_theatre_id="enable_theatre" @delete_theatre_id="delete_theatre"/>
        </div>
        <div class="container" v-if="!theatres_data">
            <h1>No Theatres have been created By this User</h1>
            <button class="btn btn-danger col-9" @click="gotoaddtheatre">Add Theatres</button>
        </div>
    </div>
</template>

<script>
import cards from '@/components/cards.vue'

export default{
    data(){
        return{
            page: 'theatres' 
        }
    },
    props: ['login'],
    components: {Cards: cards},
    computed: {
        theatres_data(){
            return this.$store.state.theatre_data
        }
    },
    methods:{
        gotoaddtheatre(){
        this.$router.push({path: '/admin/add_theatre'})
      },
      //Event based methods
      disable_theatre(e){
        let url = "http://127.0.0.1:5000/admin/disable_theatre/"
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
                        alert('Theatre Disabled!')
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
      get_movies(e){
        const path = '/admin/movies/'
        const param = e
        const final_path = path.concat(param)
        this.$router.push({path: final_path})
      },
      enable_theatre(e){
        let url = "http://127.0.0.1:5000/admin/enable_theatre/"
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
                        alert('Theatre Enabled!')
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
      delete_theatre(e){
        console.log(e)
        alert('Deleting Theatre')
      }
    },
    beforeMount(){
        this.$store.dispatch('get_theatre_data')
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