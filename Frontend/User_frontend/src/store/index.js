import { createStore } from 'vuex'

export default createStore({
  state: {
    user_login_status: false,
    users: null,
    card_data: null,
    all_booking_data: null,
    show_data:null,
    search_data:null,
    user_city: 'Bangalore',
    curr_page: null,
    role: 'User'

  },
  getters: {
    movies() {},
    all_bookings() {},
    theatre_movies() {},
    shows() {},
  },

  mutations: {
    set_user_role(state, data){
      state.role = data
    },
    set_curr_page(state, curr){
      state.curr_page = curr
    },

    set_user_city(state, user_data){
      state.user_city = user_data
    },

    set_search_data(state, user_data){
      state.search_data = user_data
    }, 

    set_show_data (state, user_data){
      state.show_data = user_data
    },

    set_movies (state, user_data) {
      if (user_data){
        state.card_data = user_data
      }else{
        state.card_data = null;
      }
    },

    set_shows(state, user_data) {
      if (user_data){
        state.card_data = user_data
      }else{
        state.card_data = null;
      }
    },
    
    set_theatre_movies(state, user_data) {
      if (user_data){
        state.card_data = user_data
      }else{
        state.card_data = null;
      }
    },
    
    set_all_bookings(state, user_data) {
      if (user_data){
        state.all_booking_data = user_data
      }else{
        state.all_booking_data = null;
      }
    },

    set_user_login_status(state, user_data) {
      if (user_data){
        state.user_login_status = true;
        state.users = user_data;
      }else{
        state.user_login_status = false;
        state.users = null;
      }   
    }
  },

  actions: {
    get_movies (context, payload) {
        const city = payload
        const url = "http://127.0.0.1:5000/get_movies/"
        const final_url = url.concat(city)
        console.log(final_url)
       
        var requestOptions = {
          method: 'GET',
        };

        fetch(final_url, requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if(user_data.message){
              context.commit('set_movies', null)
            }else{
              context.commit('set_movies', user_data);
              //console.log(user_data)
            }
            
          })

          .catch(error => console.log('error', error));
    },

    get_shows(context,e) {
        const final_url = e
        console.log(final_url)
        
        var requestOptions = {
          method: 'GET',
          //headers: myHeaders
        };

        fetch(final_url, requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if (user_data.message){
              context.commit('set_shows', null)
              alert(user_data.details)
            }else{
              context.commit('set_shows', user_data);
              //console.log(user_data)
            }  
          })

          .catch(error => console.log('error', error));
    },

    get_theatre_movies(context, e) {
        const final_url = e
        console.log(final_url)
        
        var requestOptions = {
          method: 'GET'
        };

        fetch(final_url, requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if (user_data.message){
              context.commit('set_theatre_movies', null)
              alert(user_data.details)
            }else{
              context.commit('set_theatre_movies', user_data);
              console.log(user_data)
            }  
          })

          .catch(error => console.log('error', error));
    },

    get_all_bookings(context) {
      let user = localStorage.getItem('token')
      if (user) {
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", user)
        const url = "http://127.0.0.1:5000/all_bookings"
        
        //console.log(url)
        
        var requestOptions = {
          method: 'GET',
          headers: myHeaders
        };

        fetch(url, requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if (user_data.message){
              context.commit('set_all_bookings', null)
              alert(user_data.details)
            }else{
              context.commit('set_all_bookings', user_data);
              //console.log(user_data)
            }  
          })

          .catch(error => console.log('error', error));
      }
      else{
        const user_data = null;
        context.commit('set_all_bookings', user_data);
      }
        
    },

    get_user_login_status(context) {
      let user = localStorage.getItem('token')
      if(user){
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", user)
        var requestOptions = {
          method: 'GET',
          headers: myHeaders
        };

        fetch("http://127.0.0.1:5000/get_current_user", requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if(user_data.message){
              alert(user_data.details)
              localStorage.removeItem('token')
              context.commit('set_user_login_status', null)
            }
            context.commit('set_user_login_status', user_data);
            console.log(user_data)
          })

          .catch(error => console.log('error', error));
      }
      else{
        const user_data = null;
        context.commit('set_user_login_status', user_data);
      }
      
    },

    get_show_data(context,e) {
        const url = "http://127.0.0.1:5000/get_show_details/"
        const param = e
        const final_url = url.concat(param)
        if(param){
          var requestOptions = {
            method: 'GET',
            //headers: myHeaders
          };
  
          fetch(final_url, requestOptions)
            .then(response => response.json())
            .then(result => {
              if (result.message){
                alert(result.details)
              }else{
                const user_data = result;
                context.commit('set_show_data', user_data);
              }
              
            })
            .catch(error => console.log('error', error));
        }else{
          const user_data = null
          context.commit('set_show_data', user_data);
        }
        
    },

    get_search_data(context, payload){
      const search = payload.value1
      const type = payload.value2
      const city = payload.value3
      //console.log(type)
      if(type ==='movie'){
        const url = "http://127.0.0.1:5000/search_movies/"
        //const _url = url.concat(search)
        const final_url = url.concat(search)
        console.log(final_url)
        
        var requestOptions = {
          method: 'GET'
        };

        fetch(final_url, requestOptions)
          .then(response => response.json())
          .then(result => {
            if (result.message){
              alert(result.message)
            }else{
              const user_data = result;
              context.commit('set_search_data', user_data);
              console.log(user_data)
            }
            
          })
          .catch(error => console.log('error', error));

      } else if(type==='theatres'){
        const url = "http://127.0.0.1:5000/search_theatres/"
        const final_url = url.concat(search)
        console.log(final_url)
        
        var requestOptions = {
          method: 'GET'
        };

        fetch(final_url, requestOptions)
          .then(response => response.json())
          .then(result => {
            if (result.message){
              alert(result.message)
            }else{
              const user_data = result;
              context.commit('set_search_data', user_data);
              //console.log(user_data)
            }
            
          })
          .catch(error => console.log('error', error));

      } else if(type === 'city'){
        const url = "http://127.0.0.1:5000/search_city/"
        const final_url = url.concat(search)
        console.log(final_url)
        
        var requestOptions = {
          method: 'GET'
        };

        fetch(final_url, requestOptions)
          .then(response => response.json())
          .then(result => {
            if (result.message){
              alert(result.message)
            }else{
              const user_data = result;
              context.commit('set_search_data', user_data);
            }
            
          })
          .catch(error => console.log('error', error));
           
      }else{
        const url = "http://127.0.0.1:5000/search_city_theatre/"
        const final_url = url.concat(search)
        console.log(final_url)
        
        var requestOptions = {
          method: 'GET',
        };

        fetch(final_url, requestOptions)
          .then(response => response.json())
          .then(result => {
            if (result.message){
              alert(result.message)
            }else{
              const user_data = result;
              context.commit('set_search_data', user_data);
              //console.log(user_data)
            }
            
          })
          .catch(error => console.log('error', error));
      }
        


    },

    get_user_city(context, payload){
      const user_data = payload
      context.commit('set_user_city', user_data);
    },

    get_curr_page(context, payload){
      const curr = payload
      context.commit('set_curr_page', curr)
    },

    get_user_role (context, payload){
      const data = payload
      context.commit('set_user_role', data)
    }

  },


  modules: {
  }
})
