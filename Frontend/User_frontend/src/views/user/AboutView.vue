<template>
<div class="div-des">
        <h1>Profile Page</h1>
    </div>

  <div v-if="user">
      <div class='container container_style'>
        <h1 class="header">Info Update</h1>
        <div class="form-group input-control">
          <input v-model="email" type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp"
            placeholder="Enter email">
        </div>
        <div class="form-group input-control">
          <input v-model="name" type="text" class="form-control" id="exampleInputname1" placeholder="Name">
        </div>

        <button class="btn btn-primary btn-style col-9 " @click="update">Update Profile</button>
        <button class="btn btn-danger btn-style col-9" @click="changepwd">Change_pwd</button>
      </div>

  </div>

  <div class="about" v-if="!user">
    <h1>About User Page</h1>
    <h2>You need to log in to access this page!</h2>
    <button @click="gohome" class="btn btn-danger">Go Home</button>
  </div>
</template>

<script>
export default{
  data(){
    return{
      email:null,
      name:null,
      data:null,
      updated_data:null,
    }
  },
  computed: {
    user() {
      return this.$store.state.users
    }
  },
  props: ['login'],
  mounted(){
      this.$store.dispatch('get_curr_page', 'About')
      
      {let token_ = localStorage.getItem('token')
      if(token_){
        var myHeaders = new Headers();
        myHeaders.append("x-access-token", token_)
        var requestOptions = {
          method: 'GET',
          headers: myHeaders
        };

        fetch("http://127.0.0.1:5000/get_current_user", requestOptions)
          .then(response => response.json())
          .then(result => {
            this.data = result;
            if(this.data['email']){
              this.email = this.data['email'];
              this.name = this.data['user_name'];
            }
          })

          .catch(error => console.log('error', error));
      }
      else{
        const user_data = null;
        this.$store.dispatch('get_user_login_status');
      }};

      {
      this.$store.dispatch('get_curr_page', 'About')
       }
  },
  methods: {
    gohome(){
      this.$router.push({path: '/'})
    },
    update(){
      if(this.login['user_name'] != this.name || this.login['email'] != this.email){
        //call update function here!
        const token_ = localStorage.getItem('token')
        if(token_){
          var myHeaders = new Headers();
          myHeaders.append("x-access-token", token_);
          myHeaders.append("Content-Type", "application/json");

          var raw = JSON.stringify({
            "email": this.email,
            "name": this.name
          });

          var requestOptions = {
            method: 'PUT',
            headers: myHeaders,
            body: raw
          };

          const url = "http://127.0.0.1:5000/update_user"

          fetch(url, requestOptions)
            .then(response => response.json())
            .then(result => {
              console.log(result);
              alert('Your profile has been updated!');
              this.$store.dispatch('get_user_login_status');
              //window.location.reload();
            })
            .catch(error => console.log('error', error));
        }
        
      }else{
        alert('Your profile has been updated!')
      }
    },
    changepwd(){
      const token_ = localStorage.getItem('token')
        if(token_){
          var myHeaders = new Headers();
          myHeaders.append("x-access-token", token_);

          var requestOptions = {
            method: 'PUT',
            headers: myHeaders,
          };

          fetch("http://127.0.0.1:5000/change_password", requestOptions)
            .then(response => response.json())
            .then(result => {
              const user_data = result;
              if(user_data.message === 'Success'){
                alert('An Email has been sent to you with password change link');
                console.log(user_data)
              }
              else{
                alert('There is some error! Check if celery is working properly!')
                console.log(user_data)
              }

            })
            .catch(error => console.log('error', error));
        
    }
      }
  },

}
</script>


<style scoped>
.main-container{
  min-height: 550px;
  align-items: center;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  margin: 100px
}
.container {
  width: 500px;
  height: 400px;
 
  padding-top: 85px;
  padding-left: 50px;
  padding-right: 50px;
  
  background-color: rgba(182, 176, 171, 0.5);
  align-items: justify-content+50;
  border-radius: 20px;
  box-shadow: -6px 2px 10px 0px  rgba(0, 0, 0, 0.3);
}
.input-control{
  margin:10px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}
.form-check {
  margin-right: 20px;
  margin-bottom: 10px;  
}
.form-check-label {
  font-weight: lighter;
  font-size: 15px;
}
.form-check-input{
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.3);
  margin: 10px;
}
.btn-style{
  margin: 5px;
  margin-top: 10px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}
.header{
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  text-transform: uppercase;
  border-radius: 2px;
  margin-top: 50px;
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
.div-des{
    background-color: rgb(182, 176, 171);
    align-items: start;
    padding: 10px;  
}

.container_style{
    padding-top: 20px;
    align-items: start;
    margin-top: 30px;
}
</style>