<template>
    <div class="container">
        <div class="row my-5 mx-auto d-flex justify-content-center">
            <div class="login col-md-6 col-12 ">
                <div class="log">
                    <form>
                        <h4 class="col-md-12 text-center align-top ">Admin Login</h4>
                        <div class="form-floating mb-3 col-md-12 ">
                            <input type="text" v-model="username" class="form-control" id="floatingInput" placeholder=" ">
                            <label for="floatingInput">Username</label>
                        </div>
                        <div class="form-floating col-md-12 ">
                            <input type="password" v-model="password" class="form-control" id="floatingPassword"
                                placeholder=" ">
                            <label for="floatingPassword">Password</label>
                        </div>
                        <div class="col-md-12 my-5 text-center pt-3 ">
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
    name: "AdminLogin",
    setup() {
        const username = ref('')
        const password = ref('')
        const router = useRouter()

        const handleLoginSubmit = async () => {
            try {

                const response = await fetch(`${config.url}/api/admin_login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: username.value,
                        password: password.value
                    })
                })
                const data = await response.json()
                console.log(data)

                if (response.status === 400) {
                    console.log(response);
                    // throw new Error(`${}`);
                    toast.error(data.error);
                }

                else {
                    const isAdmin = data.token
                    localStorage.setItem('isAdmin', isAdmin)
                    console.log(isAdmin)
                        if (response.status === 200) {
                            // alert("Login Successful")
                            setTimeout(() => {  router.push('/admin_home'); }, 1000);
                            toast.success('Login Successful',{position:'top-right',autoClose: 1500});  
                            
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
            username,
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


.login {
    height: 75vh;
    background: rgba(230, 253, 253, 0.279);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.log {
    padding-top: 15vh;
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


</style>