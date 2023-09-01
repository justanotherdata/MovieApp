<template>
    <div class="div-des">
        <h1>Search Result Page</h1>
    </div>
    <div class="container_style">
      <cards :card_data="search_data" :page="search_result" @trigger_get_shows="getshowdata"/>
    </div>
  
</template>

<script>
import cards from '@/components/Cards copy.vue'

export default{
  data() {
      return{
          search: null,
          message: null,
          selectedOption: 'movie',
          search_result: 'search_result'
          
      }
  },
  computed:{
    search_data(){
      return this.$store.state.search_data
    }
  },

  components: {cards},
  props: ['login'],
  methods: {
    getshowdata(e){
    const path_ = '/shows/'  
    const param = e
    const final_path = path_.concat(param)
    
    this.$router.push({path: final_path})}
  
            
  },
  mounted() {
    this.$store.dispatch('get_curr_page', 'search')
  }
}
</script>

<style scoped>

.container{
  background-color: rgba(175, 175, 175, 0.97);
  display: block;
  justify-content: space-evenly;
  height: auto;
  width: 600px;
  padding: 15px;
  border-radius: 5px;
  margin-top: 10px;
}
.container-search{
background-color: #c7c7c7f1;
width: auto;
margin-top: 20px;
margin-bottom: 20px;
padding: 15px;
}
.btn-block{
  margin-top: 1px;
  
}
.div_styling{
  margin-top: 15px;
  margin-bottom:15px;
}
.dropdown {
  position: relative;
  display: inline-block;
  margin: 0;  
} 

.div-des{
    background-color: rgb(182, 176, 171);
    align-items: start;
    padding: 10px;  
}

.container_style{
    padding-top: 40px;
    align-items: start;
}
</style>