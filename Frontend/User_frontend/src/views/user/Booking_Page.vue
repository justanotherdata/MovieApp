<template>
  <div class="div-des">
        <h1>Booking Page</h1>
    </div>
  <div v-if="login">
      <div class='container container_style' v-if="show_data">
        <h1 class="header">Booking Form</h1>
        <div class="form-group input-control">
          <p class="form-control">Movie Name: {{ show_data.movie_name }}</p>
          <p class="form-control next">Theatre Name: {{ show_data.theatre_name }}</p>
          <p class="form-control">Show Time: {{ show_data.timing }}</p>
          <p class="form-control next">City: {{ show_data.city }}</p>
          <p class="form-control">Available Seats: {{ show_data.available_seats }}</p>
          <p class="form-control next">Price(Per Tkt): {{ show_data.price_per_tkt }}</p>
        </div>
        <div class="form-group input-control">
          <input v-model="num_of_seats" type="text" class="form-control" id="exampleInputname1" placeholder="Enter Number Of Seats">
        </div>

        <button class="btn btn-primary btn-style" @click="book(Show_id, num_of_seats, show_data.price_per_tkt)">Book Tickets</button>
      </div>

  </div>

  <div class="about" v-if="!login">
    <h1>Booking Page</h1>
    <h2>You need to log in to access this page!</h2>
    <button @click="gohome" class="btn btn-danger">Go Home</button>
  </div>
</template>


<script>
export default{
  data(){
    return{
      num_of_seats: null
    }
  },
  components: {},
  props: ['login'],

  methods: {
    book(m, n, o){
      const show = m
      const seats = n
      const price = o
    if(!this.num_of_seats || this.num_of_seats>this.show_data['available_seats']){
      alert('You have not entered correct number of seats.')
    }else{
      const token_ = localStorage.getItem('token')
      if(token_){
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", token_);
        myHeaders.append("Content-Type", "application/json");

        var raw = JSON.stringify({
          "show_id": show,
          "num_of_tkts": seats,
          "price": price
        });

        var requestOptions = {
          method: 'POST',
          headers: myHeaders,
          body: raw,
        };

        fetch("http://127.0.0.1:5000/booking_cnf", requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result
            if(user_data.message === 'Success'){
              alert(user_data['details'])
              //this.$state.dispatch('get_show_data', null)
              this.$router.push({path:'/'})
            }else{
              alert(user_data['details'])
            }
          })
          .catch(error => console.log('error', error));
      }
    }
   
    }
  },
  computed:{
    Show_id(){
      return this.$route.params.show_id;
    },
    show_data(){
      return this.$store.state.show_data
    }
},
beforeMount(){
  //console.log('Dispatching get_show_data from Booking_Page')
  this.$store.dispatch('get_show_data', this.Show_id)
  this.$store.dispatch('get_curr_page', null)
},
}
</script>


<style scoped>
.container {
  margin-top: 40px;
  margin-bottom: 50px;
  padding-top: 25px;
  padding-left: 50px;
  padding-right: 50px;
  padding-bottom: 30px;
  width: 500px;
  height: auto;
  background-color: rgba(182, 176, 171, 0.5);
  align-items: justify-content;
  border-radius: 20px;
  box-shadow: -6px 2px 10px 0px  rgba(0, 0, 0, 0.3);
}
.input-control{
  margin:10px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}
.btn-style{
  margin: 5px;
  margin-top: 10px;
  width: 150px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}
.header{
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  text-transform: uppercase;
  border-radius: 2px;
  margin-top: 10px;
  margin-bottom: 10px;
  color: rgb(255, 255, 255);
  height: 50px;
  margin-bottom: 15px;
  background: #000000;
  font-weight: bold;
  font-size: 20px;
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  letter-spacing: 3px;
  display: flex;
}
.form-group {
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}
.next{
  background-color: rgb(185, 183, 180);
}

.div-des{
    background-color: rgb(182, 176, 171);
    align-items: start;
    padding: 10px;  
}

.container_style{
    padding-top: 30px;
    align-items: start;
}
</style>