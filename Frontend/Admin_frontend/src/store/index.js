import { createStore } from 'vuex'

export default createStore({
  state: {
    user_login_status: false,
    users: null,
    role: 'Admin',
    home_data: null,
    booking_data : null,
    theatre_data: null,
    movies_data: null,
    shows_data: null,
    download_url: null,

  },
  getters: {
  },

  mutations: {
    set_user_role(state, data){
      state.role = data
    },
    set_user_login_status(state, user_data) {
      if (user_data){
        state.user_login_status = !state.user_login_status;
        state.users = user_data;
      }else{
        state.user_login_status = false;
        state.users = null;
      }   
    },
    set_home_data(state, user_data) {
      if (user_data) {
        state.home_data = user_data
      }else{
        state.home_data = null
      }
    },
    set_booking_data(state, user_data){
      if(user_data){
        state.booking_data = user_data
      }else{
        state.booking_data = null
      }
    },
    set_theatre_data(state, user_data){
      if(user_data) {
        state.theatre_data = user_data
      }else{
        state.theatre_data = null
      }
    },
    set_movies_data(state, card_data){
      if(card_data){
        state.movies_data = card_data
      } else{
        state.movies_data = null
      }
    },
    set_shows_data(state, card_data){
      if(card_data){
        state.shows_data = card_data
      }else{
        state.shows_data = null
      }
    },
    set_download_url(state, card_data){
      if (card_data){
        state.download_url = card_data
      }else{
        state.download_url = null
      }
    },
    set_custom_booking_data(state, user_data){
      if(user_data){
        state.booking_data = user_data
      }else{
        state.booking_data = null
      }
    },
    set_custom_movies_data(state, card_data){
      if(card_data){
        state.movies_data = card_data
      } else{
        state.movies_data = null
      }
    },
    set_custom_shows_data(state, card_data){
      if(card_data){
        state.shows_data = card_data
      }else{
        state.shows_data = null
      }
    }

  },

  actions: {
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
            else{
              context.commit('set_user_login_status', user_data);
              //console.log(user_data)
            }
            
          })

          .catch(error => console.log('error', error));
      }
      else{
        const user_data = null;
        context.commit('set_user_login_status', user_data);
      }
      
    },

    get_user_role (context, payload){
      const data = payload
      context.commit('set_user_role', data)
    },

    get_home_data(context) {
      let user = localStorage.getItem('token')
      if(user){
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", user)
        var requestOptions = {
          method: 'GET',
          headers: myHeaders
        };

        fetch("http://127.0.0.1:5000/home_admin", requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if(user_data.message){
              alert(user_data.details)
              context.commit('set_home_data', null)
            }
            else{
              context.commit('set_home_data', user_data);
              //console.log(user_data)
            }
            
          })
          .catch(error => console.log('error', error));
      }
      else{
        const user_data = null;
        context.commit('set_home_data', user_data);
      }
    },
    get_booking_data(context) {
      let user = localStorage.getItem('token')
      if(user){
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", user)
        var requestOptions = {
          method: 'GET',
          headers: myHeaders
        };

        fetch("http://127.0.0.1:5000/admin_bookings", requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if(user_data.message){
              alert(user_data.details)
              context.commit('set_booking_data', null)
            }
            else{
              context.commit('set_booking_data', user_data);
              //console.log(user_data)
            }
            
          })
          .catch(error => console.log('error', error));
      }
      else{
        const user_data = null;
        context.commit('set_booking_data', user_data);
      }
    },

    get_theatre_data(context){
      let user = localStorage.getItem('token')
      if(user){
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", user)
        var requestOptions = {
          method: 'GET',
          headers: myHeaders
        };

        fetch("http://127.0.0.1:5000/admin_theatres", requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if(user_data.message){
              alert(user_data.details)
              context.commit('set_theatre_data', null)
            }
            else{
              context.commit('set_theatre_data', user_data);
              //console.log(user_data)
            }
            
          })
          .catch(error => console.log('error', error));
      }
      else{
        const user_data = null;
        context.commit('set_theatre_data', user_data);
      }
    },

    get_movies_data(context){
      let user = localStorage.getItem('token')
      if(user){
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", user)
        var requestOptions = {
          method: 'GET',
          headers: myHeaders
        };

        fetch("http://127.0.0.1:5000/admin_movies", requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if(user_data.message){
              alert(user_data.details)
              context.commit('set_movies_data', null)
            }
            else{
              context.commit('set_movies_data', user_data);
              //console.log(user_data)
            }
            
          })
          .catch(error => console.log('error', error));
      }
      else{
        const user_data = null;
        context.commit('set_movies_data', user_data);
      }
    },

    get_shows_data(context){
      let user = localStorage.getItem('token')
      if(user){
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", user)
        var requestOptions = {
          method: 'GET',
          headers: myHeaders
        };

        fetch("http://127.0.0.1:5000/admin_shows", requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if(user_data.message){
              alert(user_data.details)
              context.commit('set_shows_data', null)
            }
            else{
              context.commit('set_shows_data', user_data);
              //console.log(user_data)
            }
            
          })
          .catch(error => console.log('error', error));
      }
      else{
        const user_data = null;
        context.commit('set_shows_data', user_data);
      }
    },

    get_download_url(context, payload){
      const card_data = payload
      context.commit('set_download_url', card_data)
    },

    get_custom_booking_data(context, payload){
      let url = "http://127.0.0.1:5000/admin/get_bookings/"
      let param = payload
      let final_url = url.concat(param)
      //console.log(final_url)

      let user = localStorage.getItem('token')
      if(user){
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", user)
        var requestOptions = {
          method: 'GET',
          headers: myHeaders
        };

        fetch(final_url, requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if(user_data.message){
              context.commit('set_custom_booking_data', null)
              //alert(user_data.details)
            }
            else{
              context.commit('set_custom_booking_data', user_data);
              //console.log(user_data)
            }
            
          })
          .catch(error => console.log('error', error));
      }
      else{
        const user_data = null;
        context.commit('set_custom_booking_data', user_data);
      }
    },

    get_custom_movies_data(context, payload){
      let url = "http://127.0.0.1:5000/admin/get_movies/"
      let param = payload
      let final_url = url.concat(param)
      //console.log(final_url)

      let user = localStorage.getItem('token')
      if(user){
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", user)
        var requestOptions = {
          method: 'GET',
          headers: myHeaders
        };

        fetch(final_url, requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if(user_data.message){
              context.commit('set_custom_movies_data', null)
              //alert(user_data.details)
            }
            else{
              context.commit('set_custom_movies_data', user_data);
              //console.log(user_data)
            }
            
          })
          .catch(error => console.log('error', error));
      }
      else{
        const user_data = null;
        context.commit('set_custom_movies_data', user_data);
      }
    },
    get_custom_shows_data(context, payload){
      let url = "http://127.0.0.1:5000/admin/get_show/"
      let param = payload
      let final_url = url.concat(param)
      //console.log(final_url)

      let user = localStorage.getItem('token')
      if(user){
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", user)
        var requestOptions = {
          method: 'GET',
          headers: myHeaders
        };

        fetch(final_url, requestOptions)
          .then(response => response.json())
          .then(result => {
            const user_data = result;
            if(user_data.message){
              context.commit('set_custom_shows_data', null)
              //alert(user_data.details)
            }
            else{
              context.commit('set_custom_shows_data', user_data);
              //console.log(user_data)
            }
            
          })
          .catch(error => console.log('error', error));
      }
      else{
        const user_data = null;
        context.commit('set_custom_shows_data', user_data);
      }
    }

  },

  modules: {
  }
})
