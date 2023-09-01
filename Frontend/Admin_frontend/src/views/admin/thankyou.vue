<template>
    <div class="div-des">
        <h1>Bookings Page</h1>
    </div>
    <div class="container container_style">
        <h3>Your file will be downloaded automatically. If not, click <a :href="url">Download</a></h3>

        <button class="btn btn-primary col-6 btn_style" @click="gohome">Go Home</button>
    </div>
</template>

<script>
export default{
    data(){
        return{
           
        }
    },
    props: ['login'],
    computed:{
        url(){
            return this.$store.state.download_url
        }
    },
    methods:{
        gohome(){
            this.$router.push({path:'/admin/home'})
        }
    }
}
</script>

<style scoped>
.div-des{
    background-color: rgb(219, 219, 216);
    align-items: start;
    padding: 10px;   
}
.container_style{
    padding-top: 20px;
    align-items: start;
}
.btn_style{
    padding: 10px;
    padding-top: 12px;
    margin: 5px
}
</style>