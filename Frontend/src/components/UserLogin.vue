<template>
    <div class="container ">
        <div class="row d-flex align-items-center mx-0 my-lg-5 my-md-5 my-0">
            <div class="blank col-md-6 col-12 d-flex justify-content-center">
                <!-- <h3>Don't have an account? </h3> -->
                <div class="col-md-12 text-center  align-middle position-absolute top-50 start-50 translate-middle">
                    <h3>Don't have an account? </h3>
                    <!-- <router-link class="btn btn-success" to="/userregister">Register here!</router-link> -->
                    <button class="my-4  primary-button" @click="$router.push('/user_register')">Register here!</button>
                </div>
            </div>
            <div class="login col-md-6 col-12 ">
                <div class="log">
                    <form>
                        <h4 class="col-md-12 text-center ">Login</h4>
                        <div class="form-floating mb-3 col-md-12 ">
                            <input type="email" v-model="email" class="form-control" id="floatingInput" placeholder=" ">
                            <label for="floatingInput">Email address</label>
                        </div>
                        <div class="form-floating col-md-12 ">
                            <input type="password" v-model="password" class="form-control" id="floatingPassword"
                                placeholder=" ">
                            <label for="floatingPassword">Password</label>
                        </div>
                        <div class="col-md-12 text-center pt-3 ">
                            <h5>
                                <router-link style="text-decoration: none; color:rgb(63, 126, 129)" to="/forget_password">Click here! If you Forget Password</router-link>
                            </h5>
                        </div>
                        <div class="col-md-12 text-center pt-3 ">
                            <button type="submit" @click.prevent="handleLoginSubmit" id="butt" class=" primary-button">
                                <i class="bi bi-box-arrow-in-right"></i>
                                Login
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {config} from '../Constants.js';
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import VueJwtDecode from 'vue-jwt-decode'
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';



export default {
    name: "UserLogin",
    setup() {
        const email = ref('')
        const password = ref('')
        const router = useRouter()

        const handleLoginSubmit = async () => {
            try {

                const response = await fetch(`${config.url}/api/user_login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: email.value,
                        password: password.value
                    })
                })
                const data = await response.json()
                console.log(data)

                if (response.status === 400) {
                    console.log(response);
                    // throw new Error(`${toast.error(data.error)}`);
                    toast.error(data.error);
                }

                else {
                    const token = data.token
                    localStorage.setItem('token', token)
                    console.log(token)
                        if (response.status === 200) {
                            // alert("Login Successful")
                            toast.success('Login Successful',{position:'top-right',autoClose: 2000});  
                            setTimeout(() => {  router.push('/user_home'); }, 2000);
                            // router.push('/userhome')
                                                     
                        }
                        // if (response.status === 201) {
                        //     alert("Please complete your profile")
                        //     router.push('/complete-profile')
                        // }
                }

            }
            catch (error) {
                console.log("hi it's error in login")
                console.log(error)

            }
        }
        return {
            email,
            password,
            handleLoginSubmit,
        }
    },


}

</script>

<style>
.container {
    width: 100%;
    height: 100%;
}

.blank {
    height: 75vh;
    background: rgba(76, 172, 250, 0.36);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.login {
    height: 75vh;
    background: rgba(230, 253, 253, 0.279);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);

}

.log {
    padding-top: 20vh;
}

.form-floating input[type="text"],
.form-floating input[type="email"],
.form-floating input[type="password"],
.form-floating textarea {
    border: none;
    border-radius: 0;
    border-bottom: 1px solid #a9b0b7;
    background-color: rgba(255, 255, 255, 0);
}

button{
  padding: 4% 8%;
  border-radius: 10px;
  border: none;
  background-color: #ff8f8f;
  font-size: 1.5rem;
  font-weight: bold;
  color: rgb(74,24,24);
  transition: all 0.5s ease;
}

</style>