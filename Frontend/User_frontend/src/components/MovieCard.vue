<template>
    <div class="movie-card" v-if="!page">
      <h2>{{ movie.name }}</h2>
      <p class="theatre">Theatre: {{ movie.theatre }}</p>
      <p class="seats">Available Seats: {{ movie.seats }}</p>
      <router-link :to="`/shows/${movie.name}`" class="button">Go to Shows</router-link>
    </div>

    <div class="movie-card" v-if="page">
      <p>Booking_Id: {{ card_data.id }}</p>
      <p class="movie">Movie: {{ card_data.mov_name }}</p>
      <p class="theatre">Theatre: {{ card_data.the_name }}</p>
      <p class="seats">Available Seats: {{ card_data.num_of_tkts }}</p>
      <p class="seats">Timing: {{ card_data.timing }}</p>
      <button v-if="card_data.active_status" class="btn btn-danger" @click="cancelbooking(card_data.id)">Cancel</button>
      <button v-if="!card_data.active_status" class="btn btn-primary" disabled>Cancel</button>
    </div>
  </template>
  
  <script>
  export default {
    emits:['cancel_bookingid'],
    props: {
      movie: Object,
      card_data: Object,
      page: String // Define a prop to receive movie data from the parent component
    },
    methods:{
      cancelbooking(e){
        console.log(e)
        this.$emit('cancel_bookingid', e)
      }
    }
  };
  </script>
  

<style scoped>

.movie-card {
  background-color: #f4f4f4;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin: 10px;
  width: calc(33.33% - 20px); /* Adjust for three cards in a row */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

  .theatre, .seats {
  color: #777;
  margin: 5px 0;
}

.button {
  display: inline-block;
  background-color: #3498db;
  color: #fff;
  padding: 8px 15px;
  border-radius: 4px;
  text-decoration: none;
  transition: background-color 0.3s;
}

.button:hover {
  background-color: #2980b9;
}
</style>

  