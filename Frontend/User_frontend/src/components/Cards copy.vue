<template>
    <div v-if="page === 'home'">
        <div v-if="card_data">
            <div v-for="data in card_data" :key="data.id"> 
            <div class="card custom-card">
                <div class="card-body">
                    <h5 class="card-title custom-card-items">
                        Movie: {{ data['mov_name'] }}
                        <p class="card-title">Rating: {{ data['mov_rating'] }}</p>
                        <button class="btn btn-danger btn-custom" @click="gotoshows(data.id)"> Get Show </button>
                    </h5>  
                </div>
            </div>
        </div>
        </div>
        <div v-else>
            <h2>No movies to display in this city</h2>
        </div>

    </div>


    <div v-if="page === 'shows'">
        <div v-if="card_data">
            <h3 v-if="card_data['Mov_Name']">Showing results for {{ card_data['Mov_Name'] }}</h3>
            <h4 v-if="card_data['Mov_Name']">Rating: {{card_data['Mov_Rating'] }}</h4>
        <div v-for="data in card_data['show_details']" :key="data.Theatre_Id"> 
            <div class="card custom-card">
                <div class="card-body">
                    <h5 class="card-title custom-card-items">
                        <p class="card-title" v-if="data.Theatre_Id">
                            <router-link :to="{name:'Theatre_movies', params: { The_Id: data.Theatre_Id }}">
                                {{ data.Theatre_Name }}
                            </router-link>
                        </p>
                        <div v-for="show in data['all_show']" :key="show">
                            <p>Seats: {{ show['available'] }}</p>
                            <button class="btn btn-danger btn-custom" @click="gotobooking(show.show_id)"> {{ show.time }} </button>
                        </div>
                        
                    </h5> 
                </div>
            </div>
        </div>
        </div>
        <div v-else>
            <h2>No shows for this movie currently!</h2>
        </div>
    </div>
 

    <div v-if="page === 'theatres'">
        <div v-if="card_data">
            <div v-for="data in card_data" :key="data.id"> 
            <div class="card custom-card">
                <div class="card-body">
                    <h5 class="card-title custom-card-items">
                        Movie: {{ data['mov_name'] }}
                        <p class="card-title">Rating: {{ data['mov_rating'] }}</p>
                        <button class="btn btn-danger btn-custom" @click="gotoshows(data.id)"> Get Show </button>
                    </h5>  
                </div>
            </div>
        </div>
        </div>
        <div v-else>
            <h2>No movies to display in this city</h2>
        </div>
    </div>

    <div v-if="page === 'search_result'">
        <div v-if="card_data">
            <div v-for="data in card_data" :key="data.id"> 
            <div class="card custom-card">
                <div class="card-body">
                    <h5 class="card-title custom-card-items">
                        Movie: {{ data['mov_name'] }}
                        <p class="card-title">Rating: {{ data['mov_rating'] }}</p>
                        <button class="btn btn-danger btn-custom" @click="gotoshows(data.id)"> Get Show </button>
                    </h5>  
                </div>
            </div>
        </div>
        </div>
        <div v-else>
            <h2>No movies to display in this city</h2>
        </div>
    </div>



            
</template>

<script>
export default{
  emits: ['trigger_get_shows', 'trigger_show_detail'],  
  data() {
    return{
        show_id: null
    }
    
  },  
  props: ['card_data', 'page'],
  methods: {
    gotoshows(e) {
        
        this.$emit('trigger_get_shows', e)
       

    },
    gotobooking(e) {
        this.$emit('trigger_show_detail', e)
    }
    
  },
  computed: {
    
  }
  
}
</script>

<style>
.custom-card{
    padding: 0.15rem;
    margin: 1rem;
}
.custom-card-items{
   padding-left: 1rem;
  padding-right: 1rem;
  max-width: 100%;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  background-color: #ebebebad;
  border-radius: 5px;
  padding-top: 40px;
  align-items: center;
  padding-bottom: 40px;
  margin-bottom: 10px;
  margin-left: auto;
  margin-right: auto;
}
.text-color{
    color: black;
}
.btn-custom{
    padding-top: auto;
}
</style>