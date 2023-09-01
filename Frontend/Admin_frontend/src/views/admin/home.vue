<template>
    <div class="div-des">
        <h1>Home Page</h1>
    </div>
    <div class="container container_style">
        <h1 v-if="login">Welcome back, {{ login['user_name'] }}!</h1>
        <div class="movie-cards container">
        <Cards :page="page" v-for="(data, index) in home_data" :key="index" :card_data="data"/>
    </div>

    <button class="btn btn-dark col-6 btn_style" @click="download"><h4>Download Report</h4></button>
    </div>
    
</template>

<script>
import cards from '@/components/cards.vue'

export default{
    data(){
        return{
            page: 'home'
        }
    },
    props: ['login'],
    components:{Cards: cards},
    computed:{
        home_data(){
            return this.$store.state.home_data
        }
    },
    methods:{
        download(){
            let user = localStorage.getItem('token')
            if(user){
                var myHeaders = new Headers();
                myHeaders.append("x-access-token", user)
                var requestOptions = {
                method: 'GET',
                headers: myHeaders
                };

                fetch("http://127.0.0.1:5000/generate_and_send_csv_", requestOptions)
                .then(response => response.json())
                .then(result => {
                    const user_data = result;
                    if(user_data.message){
                    alert(user_data.details)
                    }
                    else{
                    //console.log(user_data)
                    const absoluteURL = `http://${user_data.url}`;
                    this.$store.dispatch("get_download_url", absoluteURL)
                    this.$router.push({path:'/admin/thankyou'})
                    setTimeout(() => {
                        window.open(absoluteURL, '_blank');
                    }, 1000);
                    
                    }
                    
                })

                .catch(error => console.log('error', error));
                    }
        }
    },
    beforeMount() {
        this.$store.dispatch("get_home_data")
    }
}
</script>

<style scoped>
.movie-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.btn_style{
    padding: 10px;
    padding-top: 15px;
    margin: 8px
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