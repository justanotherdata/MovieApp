<template>
    <div class="div-des">
        <h1>Add Theatres Page</h1>
    </div>
    <div class="container container_style">
            <div class="mb-3">
                <label for="Theatre" class="form-label"><h3>Theatre Name</h3></label>
                <input v-model= 'theatre' type="text" class="form-control" id="Theatre" aria-describedby="Theatre">
            </div>
            <div class="mb-3">
                <label for="location" class="form-label"><h3>City Name</h3></label>
                <input v-model= 'location' type="text" class="form-control" id="location">
            </div>
            <button @click = "add_theatre" type ='button' class="btn btn-danger col-6 btn_style"><h5>Add Theatre</h5></button>
    </div>
</template>

<script>
export default{
    data(){
        return{
            theatre: null,
            location: null
        }
    },
    props: ['login'],
    methods:{
        add_theatre(){
            if(this.theatre && this.location){
                let user_token = localStorage.getItem('token')
                //console.log(user_token)
                if(user_token){
                    var myHeaders = new Headers();
                    myHeaders.append("x-access-token", user_token);
                    myHeaders.append("Content-Type", "application/json");

                    var raw = JSON.stringify({
                    "The_Name": this.theatre,
                    "The_Location": this.location
                    });

                    var requestOptions = {
                    method: 'POST',
                    headers: myHeaders,
                    body: raw
                    };
                    //console.log('Works Till here!')
                    fetch("http://127.0.0.1:5000/add_theatre", requestOptions)
                    .then(response => response.json())
                    .then(result => {
                       const data = result;
                       if (data.message === 'Success') {
                        alert('User added!')
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
                alert('Fill both Theatre and Location to proceed!')
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