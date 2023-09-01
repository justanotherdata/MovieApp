<template>
  <div class="div-des">
        <h1>Signup Page</h1>
    </div>

    <div class="container container_style" v-if="!user_login">
        <form>
            <div class="mb-3">
                <label for="name" class="form-label"><h5>Name</h5></label>
                <input type="text" class="form-control" id="name" aria-describedby="nameHelp" v-model="name">
            </div>
            <div class="mb-3">
                <label for="exampleInputEmail1" class="form-label"><h5>Email</h5></label>
                <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model="email">
            </div>
            <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label"><h5>Password</h5></label>
                <input type="password" class="form-control" id="exampleInputPassword1" v-model="password">
            </div>
            <div class="mb-3">
                <label for="exampleconfirmPassword1" class="form-label"><h5>Confirm Password</h5></label>
                <input type="password" class="form-control" id="exampleconfirmPassword1" v-model="cnf_password">
            </div>
            <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="exampleCheck1" v-model="remember">
                <label class="form-check-label" for="exampleCheck1">Remember me</label>
            </div>
            <button type="button" class="btn btn-primary col-6" @click="signup">Submit</button>
        </form>
    </div>

    <div v-if="user_login">
        <p>You are already logged in!</p>
        <button @click="gohome">Go Home</button>
    </div>

</template>

<script>
export default{
  data(){
    return{
      name:null,
      password:null,
      cnf_password:null,
      email:null,
      remember:null,
      data:null
    }
  },
  computed:{
    user_login(){
      return this.$store.state.user_login_status
    }
  },
  components: {},
  props: ['login'],
  methods: {
    gohome(){
      this.$router.push({path:'/'})
    },

    signup() {
      if(this.password == this.cnf_password){
        //Signup Logic Here
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        var raw = JSON.stringify({
        "email": this.email,
        "password": this.password,
        "name": this.name
});

      var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw
      };

      fetch("http://127.0.0.1:5000/create_user", requestOptions)
        .then(response => response.json())
        .then(result => {
          this.data = result;
          if(this.data['token']){
            //Deleting if any past tokens exist
            localStorage.removeItem('token')
            //Setting up new token
            localStorage.setItem('token', this.data['token'])
            alert(this.data['message'])
            this.data = null;
            this.email = null;
            this.password = null;
            this.cnf_password = null;
            this.$store.dispatch('get_user_login_status')
            this.$router.push({path:'/'})
            
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
      }
      
      else{
        alert('Password and confirm_password do not match')
      }
       
        
    }
  },
  mounted(){
    this.$store.dispatch('get_curr_page', 'signup')
  }
}
</script>

<style scoped>
.div-des{
    background-color: rgb(182, 176, 171);
    align-items: start;
    padding: 10px;  
}

.container_style{
    padding-top: 20px;
    align-items: start;
}
</style>