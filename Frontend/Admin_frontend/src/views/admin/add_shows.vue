<template>
    <div class="div-des">
        <h1>Add Shows Page</h1>
    </div>
    <div class="container container_style">
            <div class="mb-3">
                <label class="form-label"><h3>Choose a City</h3></label>
                <div class="dropdown">
                    <span class="dropdown-toggle btn btn-light col-9" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <a v-if="!city">City List</a>
                        <a v-if="city">{{ city }}</a>
                    </span>

                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                        <li v-for="cit in cities" :id="cit">
                            <a  class="dropdown-item dropdown" value="movie" @click="choose_city(cit)">{{ cit }}</a>
                        </li>
                    </ul>
                </div>
            </div>


            <div class="mb-3">
                <label class="form-label"><h3>Choose a Movie</h3></label>
                <div class="dropdown">

                    <span class="dropdown-toggle btn btn-light col-9" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <a v-if="!movie">Movie List</a>
                        <a v-if="movie">{{ movie }}</a>
                    </span>

                    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <li v-for="mov in movies" :id="mov.mov_id">
                            <a  class="dropdown-item dropdown" value="movie" @click="choose_movie(mov.mov_name, mov.mov_id)">{{ mov.mov_name }}</a>
                        </li>
                    </ul>
                </div>
            </div>


            <div class="mb-3">
                <label class="form-label"><h3>Choose a Theatre</h3></label>
                <div class="dropdown">

                    <span class="dropdown-toggle btn btn-light col-9" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <a v-if="!theatre">Theatre List</a>
                        <a v-if="theatre">{{ theatre }}</a>
                    </span>

                    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <li v-for="the in theatres" :id="the.the_id">
                            <a  class="dropdown-item dropdown" value="theatre" @click="choose_theatre(the.the_name, the.the_id)">{{ the.the_name }}</a>
                        </li>
                    </ul>
                </div>
            </div>

            <div class="mb-3">
                <label for="time" class="form-label"><h3>Enter Time</h3></label>
                <div>
                    <input v-model= 'time' type="text" class="form-control btn btn-light col-9 form-style" id="time" aria-describedby="time">
                </div>  
            </div>

            <div class="mb-3">
                <label for="seats" class="form-label"><h3>Enter Number Of Seats</h3></label>
                <div>
                    <input v-model= 'seats' type="text" class="form-control btn btn-light col-9 form-style" id="seats" aria-describedby="seats">
                </div>  
            </div>
            
            <button @click = "add_show" type ='button' class="btn btn-danger col-6 btn_style"><h5>Add Show</h5></button>
    </div>
</template>

<script>
export default{
    data(){
        return{
            theatre: null,
            movie: null,
            city: null,
            movie: null,
            theatre: null,
            cities: null,
            movies: null,
            theatres: null,
            the_id: null,
            mov_id:null,
            time: null,
            seats: null

        }
    },
    props: ['login'],
    computed:{
    },
    methods:{
        add_show(){
            if(this.time && this.seats){
                let user_token = localStorage.getItem('token')
                //console.log(user_token)
                if(user_token){
                    var myHeaders = new Headers();
                    myHeaders.append("x-access-token", user_token);
                    myHeaders.append("Content-Type", "application/json");

                    var raw = JSON.stringify({
                    "The_Id": this.the_id,
                    "Mov_Id": this.mov_id,
                    "Total_Seats": this.seats,
                    "Show_Time": this.time
                    });

                    var requestOptions = {
                    method: 'POST',
                    headers: myHeaders,
                    body: raw
                    };
                    //console.log('Works Till here!')
                    fetch("http://127.0.0.1:5000/add_show", requestOptions)
                    .then(response => response.json())
                    .then(result => {
                       const data = result;
                       if (data.message === 'Success') {
                        alert('Show added!')
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
                alert('Fill both Num_of_seats and time to proceed!')
            }
        },
        choose_city(e){
            let param = e
            this.city = param

            let url = "http://127.0.0.1:5000/admin_city_theatre/"
            let final_url = url.concat(e)
            
            let user = localStorage.getItem('token')
                if(user){
                var myHeaders = new Headers();
                myHeaders.append("x-access-token", user)
                var requestOptions = {
                method: 'GET',
                headers: myHeaders
                };
                console.log(final_url)
                fetch(final_url, requestOptions)
                .then(response => response.json())
                .then(result => {
                    const user_data = result;
                    if(user_data.message){
                    alert(user_data.details)
                    }
                    else{
                       //console.log(user_data)
                       this.theatres = user_data
                    }
                    
                })
                .catch(error => console.log('error', error));
            }
            else{
                alert('You are Not Logged In')
            }
            
        },
        choose_movie(e, m){
            let param = e
            let id = m
            console.log(param, id)
            this.mov_id = id
            this.movie = param
        },
        choose_theatre(e,m){
            let param = e
            let id = m
            this.the_id = id
            this.theatre = param
            console.log(param, id)
        },
    },
    beforeMount(){
        let user = localStorage.getItem('token')
        if(user){
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", user)
        var requestOptions = {
          method: 'GET',
          headers: myHeaders
        };

        fetch("http://127.0.0.1:5000/admin_city_movies", requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if(user_data.message){
              alert(user_data.details)
            }
            else{
                //console.log('Goes Here!')
                const _city_ = user_data[0]['city']
                
                //console.log(_city_)
              if (_city_.length > 0){
                this.cities = _city_
              }else{
                alert('No theatres! You need to add theatre first')
                this.$router.push({path: '/admin/add_theatre'})
              };
              
              const _movie_ = user_data[1]['movie']
              if (_movie_.length > 0){
                this.movies = _movie_
              }else{
                alert('No theatres! You need to add theatre first')
                this.$router.push({path: '/admin/add_movie'})
              };
              //console.log(user_data)
            }
            
          })
          .catch(error => console.log('error', error));
      }
      else{
        alert('You are Not Logged In')
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
.form-style{
    width: 75%;
    align-self: center;
    cursor: text;
}
</style>