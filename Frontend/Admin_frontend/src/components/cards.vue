<template>
    <div class="home" v-if="page === 'home'">
      <h1>{{ card_data.name }}</h1>
      <p>You have {{ card_data.Count }} active {{ card_data.name }}</p>
      <div v-if=" card_data.name  === 'Shows'">
        <button class="btn btn-danger btn_style" @click="gotoshow">Shows</button>
      </div>

      <div v-if=" card_data.name  === 'Theatres'">
        <button class="btn btn-danger btn_style" @click="gototheatre">Theatres</button>
      </div>

      <div v-if=" card_data.name  === 'Movies'">
        <button class="btn btn-danger btn_style" @click="gotomovie">Movies</button>
      </div>

      <div v-if=" card_data.name  === 'Bookings'">
        <button class="btn btn-danger btn_style" @click="gotobooking">Bookings</button>
      </div>
    </div>

    <div class="movie-card" v-if="page === 'booking' || page === 'custom_booking'">
      <h3>Booking_Id: {{ card_data.Booking_Id }}</h3>
      <p class="movie">Movie: {{ card_data.Movie_Name }}</p>
      <p class="theatre">Theatre: {{ card_data.Theatre_Name }}</p>
      <p class="theatre">City: {{ card_data.Location }}</p>
      <p class="seats">Booked Seats: {{ card_data.Num_of_seats }}</p>
      <p class="seats">Timing: {{ card_data.Timing }}</p>
      <p class = "seats" v-if="card_data.Cancellation_Reason">Cancellation Reason: {{ card_data.Cancellation_Reason }}</p>
      <button v-if="!card_data.Cancellation_Status" class="btn btn-danger col-6" @click="cancelbooking(card_data.Booking_Id)">Cancel Booking</button>
      <button v-if="card_data.Cancellation_Status" class="btn btn-primary col-6" disabled>Cancel Booking</button>
    </div>

    <div class="movie-card" v-if="page === 'theatres'">
      <h3>Theatre_Id: {{ card_data.Theatre_Id }}</h3>
      <p class="theatre">Theatre: {{ card_data.Theatre_Name }}</p>
      <p class="seats">Location: {{ card_data.Theatre_Location }}</p>
      
      <div v-if="card_data.Theatre_Status">
        
        <button class="btn btn-primary col-9 btn_style" @click="getmovies(card_data.Theatre_Id)">Get Movies</button>
        <button class="btn btn-warning col-9 btn_style" @click="disable_theatre(card_data.Theatre_Id)">Disable Theatre</button>
      </div>

      <div v-if="!card_data.Theatre_Status">
        <button class="btn btn-success col-9 btn_style" @click="enable_theatre(card_data.Theatre_Id)">Enable Theatre</button>
        <button class="btn btn-danger col-9 btn_style" @click="deletetheatre(card_data.Theatre_Id)" disabled>Delete Theatre</button>
      </div>
      
    </div>

    <div class="movie-card" v-if="page === 'movies' || page === 'custom_movies'">
      <h3>Movie_Id: {{ card_data.Mov_Id }}</h3>
      <p class="theatre">Movie: {{ card_data.Mov_Name }}</p>
      <p class="seats">Rating: {{ card_data.Mov_Rating }}</p>
      
      <div v-if="card_data.Mov_Status">
        <button class="btn btn-primary col-9 btn_style" @click="getshows(card_data.Mov_Id)">Get Shows</button>
        <button class="btn btn-warning col-9 btn_style" @click="disable_movie(card_data.Mov_Id)">Disable Movie</button>
      </div>

      <div v-if="!card_data.Mov_Status">
        <button class="btn btn-success col-9 btn_style" @click="enable_movie(card_data.Mov_Id)">Enable Movie</button>
        <button class="btn btn-danger col-9 btn_style" @click="deletemovie(card_data.Mov_Id)" disabled>Delete Movie</button>
      </div>
      
    </div>

    <div class="movie-card-shows" v-if="page === 'shows' || page === 'custom_shows'">
      <h3>Show_Id: {{ card_data.Show_Id }}</h3>
      <p class="theatre">Movie: {{ card_data.Mov_Name }}</p>
      <p class="seats">Rating: {{ card_data.Mov_Rating }}</p>
      <p class="seats">Theatre: {{ card_data.The_Name }}</p>
      <p class="seats">Location: {{ card_data.Location }}</p>
      <p class="seats">Timing: {{ card_data.Show_Time }}</p>
      
      <div v-if="card_data.Show_Status">
        <button class="btn btn-primary btn_style" @click="getbookings(card_data.Show_Id)">Get Bookings</button>
        <button class="btn btn-warning btn_style" @click="disable_show(card_data.Show_Id)">Disable Show</button>
      </div>

      <div v-if="!card_data.Show_Status">
        <button class="btn btn-success btn_style" @click="enable_show(card_data.Show_Id)">Enable Show</button>
        <button class="btn btn-danger btn_style" @click="deleteshow(card_data.Show_Id)">Delete Show</button>
      </div>
      
    </div>


  </template>
  
  <script>
  export default {
    emits:['disable_theatre_id', 'get_movies_the_id', 'enable_theatre_id', 'delete_theatre_id',
            'disable_movie_id', 'get_show_movie_id', 'enable_movie_id', 'delete_movie_id',
            'disable_show_id', 'get_bookings_show_id', 'enable_show_id','delete_show_id', 'cancel_booking_id'
          ],
    props: {
      card_data: Object,
      page: String // Define a prop to receive movie data from the parent component
    },
    methods:{
      gotobooking(){
        this.$router.push({path:'/admin/bookings'})
      },
      gotoshow(){
        this.$router.push({path:'/admin/shows'})
      },
      gotomovie(){
        this.$router.push({path:'/admin/movies'})
      },
      gototheatre(){
        this.$router.push({path:'/admin/theatres'})
      },

      //Emitting events
      //For Theatres Page
      disable_theatre(e){
        this.$emit('disable_theatre_id', e)
      },
      getmovies(e){
        this.$emit('get_movies_the_id', e)
      },
      enable_theatre(e){
        this.$emit('enable_theatre_id', e)
      },
      deletetheatre(e){
        this.$emit('delete_theatre_id', e)
      },

      //For Movies Page
      disable_movie(e){
        this.$emit('disable_movie_id', e)
      },
      getshows(e){
        this.$emit('get_show_movie_id', e)
      },
      enable_movie(e){
        this.$emit('enable_movie_id', e)
      },
      deletemovie(e){
        this.$emit('delete_movie_id', e)
      },

      //For Shows Page
      disable_show(e){
        this.$emit('disable_show_id', e)
      },
      getbookings(e){
        this.$emit('get_bookings_show_id', e)
      },
      enable_show(e){
        this.$emit('enable_show_id', e)
      },
      deleteshow(e){
        this.$emit('delete_show_id', e)
      },

      //For Bookings Page
      cancelbooking(e){
        this.$emit('cancel_booking_id', e)
      }
    }
  };
  </script>
  

<style scoped>

.home {
  background-color: #f4f4f4;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 25px;
  margin: 10px;
  width: calc(50% - 80px); /* Adjust for three cards in a row */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.movie-card {
  background-color: #f4f4f4;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin: 10px;
  width: calc(33.33% - 20px); /* Adjust for three cards in a row */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.movie-card-shows{
  background-color: #f4f4f4;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin: 10px;
  width: calc(25% - 30px); /* Adjust for three cards in a row */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

  .theatre, .seats {
  color: #777;
  margin: 5px 0;
}

.btn_style {
  margin:5px;
  padding-left: 15px;
  padding-right: 15px;
}

.button:hover {
  background-color: #2980b9;
}
</style>

  