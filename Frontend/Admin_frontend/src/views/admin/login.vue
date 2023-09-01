<template>
  <div class="div-des">
        <h1>Login Page</h1>
    </div>
    <div class="container container_style" v-if="!user_login">

        <form>
            <div class="mb-3">
                <label for="exampleInputEmail1" class="form-label"><h3>Email</h3></label>
                <input v-model= 'email' type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
            </div>
            <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label"><h3>Password</h3></label>
                <input v-model= 'password' type="password" class="form-control" id="exampleInputPassword1">
            </div>
            <div class="mb-3 form-check">
                <input v-model= 'isactive' type="checkbox" class="form-check-input" id="exampleCheck1">
                <label class="form-check-label" for="exampleCheck1">Remember me</label>
            </div>
            <button @click= 'login_' type ='button' class="btn btn-primary">Login</button>
        </form>
    </div>

    <div v-if="user_login">
    <p>You are already logged in!</p>
    <button @click="gohome">Go Home</button>
    </div>
</template>

<script>
export default {
  data() {
    return {
      email: null,
      password: null,
      isactive: false,
      data: null
    }
  },
  props: ['login'],
  computed:{
    user_login(){
      return this.$store.state.user_login_status
    },
    user_role(){
        return this.$store.state.role
    }
  },
  methods: {
    gohome(){
      this.$router.push({path:'/admin/login'})
    },

    login_(){
      if (this.email && this.password){
        //console.log('We will login from here!')
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        var raw = JSON.stringify({
        "email": this.email,
        "password": this.password
        });

      var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw
      };

      fetch("http://127.0.0.1:5000/login_admin", requestOptions)
        .then(response => response.json())
        .then(result => {
          this.data = result;
          if(this.data['token']){
            localStorage.setItem('token', this.data['token'])
            this.data = null;
            this.email = null;
            this.password = null;
            this.$store.dispatch('get_user_login_status')
            this.$store.dispatch('get_user_role', 'Admin')
            this.$router.push({path:'/admin/home'})
            //alert('You have been logged in!')
          }else{
            const err = this.data['message'];
            const msg = this.data['details'];
            alert(err + ': ' + msg)
            console.log(this.data)
          }
          
          //window.location.reload()
        })
        .catch(error => {
          console.log(error)
          if (error=='TypeError: Failed to fetch'){
            alert('Failed to fetch from the backend! Check if your backend is live!')
          }else{
            alert('Please enter valid credentials!')
          }
          
        });
        //alert('User will be logged in from here!')
      }
      
      else{
        alert('Please enter email and password to login!')
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
</style>