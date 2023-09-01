<template>
    <div class="div-des">
        <h1>Custom Movies Page</h1>
    </div>
    <div class="container container_style">
        <h3 v-if="theatre_id">All Movies for Theatre_id: {{ theatre_id }}</h3>
        <div class="movie-cards container" v-if="movies_data">
            <Cards :page="page" v-for="(data, index) in movies_data" :key="index" :card_data="data" @disable_movie_id = 'disable_movie' @get_show_movie_id="get_show" @enable_movie_id="enable_movie" @delete_movie_id="delete_movie"/>
            
        </div>
        <div class="container" v-if="!movies_data">
            <h3>No movies running currently for this theatre!</h3>
            <button class="btn btn-dark col-6 btn_style" @click="gototheatre"><h5>Go Back To Theatre</h5></button>
        </div>
    </div>
</template>

<script>
import cards from '@/components/cards.vue'

export default{
    data(){
        return{
            page: 'custom_movies' 
        }
    },
    props: ['login'],
    components: {Cards: cards},
    computed: {
        movies_data(){
            return this.$store.state.movies_data
        },
        theatre_id(){
            return this.$route.params.theatre_id;
        }
    }, 
    methods:{
      gototheatre(){
        this.$router.push({path: '/admin/theatres'})
      },  

      gotoaddmovie(){
        this.$router.push({path: '/admin/add_movie'})
      },

      //Event based methods
      disable_movie(e){
        let url = "http://127.0.0.1:5000/admin/disable_movie/"
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
                        alert('Movie Disabled!')
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
      get_show(e){
        const path = '/admin/shows/'
        const param = e
        const final_path = path.concat(param)
        this.$router.push({path: final_path})
      },
      enable_movie(e){
        let url = "http://127.0.0.1:5000/admin/enable_movie/"
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
                        alert('Movie Enabled!')
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
      delete_movie(e){
        console.log(e)
        alert('Deleting Movie')
      },
    },
    beforeMount(){
        this.$store.dispatch('get_custom_movies_data', this.theatre_id)
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