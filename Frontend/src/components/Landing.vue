<template>
  <div class="container my-auto d-flex align-content-center" style="right: 0px;left: 0px;">
    <div class="row mt-5">
      <div class="col-12 col-lg-7 mx-auto my-auto text-center">
        <h1 class=" text_shadows fw-bold lh-base ">Ticket Show Application </h1>
      </div>
      <!-- <div class="col-sm-10">
      </div> -->
      <div class="col-8 col-lg-4  m-auto  mx-s-5 login-buttons">

        <button class="my-4 primary-button" @click="$router.push('/user_login')">Login</button>

        <button class="my-4 primary-button" @click="$router.push('/user_register')">Register</button>
    
        <button class="my-4 primary-button" @click="$router.push('/admin_login')">Admin</button>
        
      </div>
    </div>
  </div>
</template>

<script >

</script>

<style scoped>
.container{
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  position: absolute;
}
.login-buttons{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 50%;
  /* width: 35%; */
  border-radius: 10px;
  background-color: #ffe5e55e;
  -webkit-box-shadow: 0px 28px 65px 14px rgba(74,24,24,0.5);
  -moz-box-shadow: 0px 28px 65px 14px rgba(74,24,24,0.5);
  box-shadow: 0px 28px 65px 14px rgba(74,24,24,0.5);
}

/* button{
  padding: 4% 8%;
  border-radius: 10px;
  border: none;
  background-color: #ff8f8f;
  font-size: 1.5rem;
  font-weight: bold;
  color: rgb(74,24,24);
  transition: all 0.5s ease;
} */

.animate-charcter {
    text-transform: uppercase;
    background-image: linear-gradient(-225deg,
            #231557 0%,
            #44107a 29%,
            #ff1361 67%,
            #fff800 100%);
    background-size: auto auto;
    background-clip: border-box;
    background-size: 50% auto;
    color: #fff;
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: textclip 2s linear infinite;
    display: inline-block;
    font-size: 6vh;
}

@keyframes textclip {
    to {
        background-position: 200% center;
    }
}
</style>