<template>
    <div class="div-des">
        <h1>Add Movie Page</h1>
    </div>
    <div class="container container_style">
            <div class="mb-3">
                <label for="Movie" class="form-label"><h3>Movie Name</h3></label>
                <input v-model= 'movie' type="text" class="form-control" id="Movie" aria-describedby="Movie">
            </div>
            <div class="mb-3">
                <label for="rating" class="form-label"><h3>Movie Rating</h3></label>
                <input v-model= 'rating' type="text" class="form-control" id="rating">
            </div>
            <button @click = "add_movie" type ='button' class="btn btn-danger col-6 btn_style"><h5>Add Movie</h5></button>
    </div>
</template>

<script>
export default{
    data(){
        return{
            movie: null,
            rating: null
        }
    },
    props: ['login'],
    methods:{
        add_movie(){
            if(this.movie && this.rating){
                let user_token = localStorage.getItem('token')
                //console.log(user_token)
                if(user_token){
                    var myHeaders = new Headers();
                    myHeaders.append("x-access-token", user_token);
                    myHeaders.append("Content-Type", "application/json");

                    var raw = JSON.stringify({
                    "Mov_Name": this.movie,
                    "Mov_Rating": this.rating
                    });

                    var requestOptions = {
                    method: 'POST',
                    headers: myHeaders,
                    body: raw
                    };
                    //console.log('Works Till here!')
                    fetch("http://127.0.0.1:5000/add_movie", requestOptions)
                    .then(response => response.json())
                    .then(result => {
                       const data = result;
                       if (data.message === 'Success') {
                        alert('Movie added!')
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
            else{
                alert('Fill both Movie_Name and Rating to proceed!')
            }
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
    padding: 5px;
    padding-top: 10px;
    margin: 5px
}
</style>