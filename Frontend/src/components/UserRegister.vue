<template>
   <div class="container">
        <div class="row align-items-center mx-0 my-5">
            <div class="register col-md-6 col-12 ">
                <div class="reg">
                    <form>
                        <h4 class="col-md-12 text-center ">Register</h4>
                        <div class="form-floating col-md-12  mb-3">
                            <input type="text" class="form-control" v-model="name" id="floatingInput" placeholder=" "
                                required />
                            <label for="floatingInput">Name</label>
                        </div>
                        <div class="form-floating col-md-12  mb-3">
                            <input type="email" class="form-control" v-model="email" id="floatingInput" placeholder=" "
                                required />
                            <label for="floatingInput">Email address</label>
                        </div>
                        <div class="form-floating col-md-12  mb-3">
                            <input type="password" class="form-control" v-model="password" id="floatingPassword"
                                placeholder=" " required />
                            <label for="floatingPassword">Password</label>
                        </div>
                        <div class="form-floating col-md-12  mb-3">
                            <input type="password" class="form-control" v-model="password_confirm" id="floatingPassword"
                                placeholder=" " required />
                            <label for="floatingPassword">Password confirm</label>
                        </div>
                        <div class="col-md-12 text-center pt-1">
                            <button type="submit" @click.prevent="handleSubmit" id="butt"
                                class="primary-button">Register</button>
                        </div>
                    </form>
                </div>
            </div>
            <div class="blank col-md-6 col-12 d-flex justify-content-center">
                <!-- <h3>Don't have an account? </h3> -->
                <div class="col-md-12 text-center position-absolute top-50 start-50 translate-middle">
                    <h3>If you have an account? </h3>
                    <!-- <router-link class="btn btn-success" to="/userlogin">Login here!</router-link> -->
                    <button class=" primary-button" @click="$router.push('/user_login')">Login here!</button>
                </div>
            </div>
        </div>
        <!-- {{ name }}
        {{ email }} -->
    </div>
</template>

<script>
import {config} from '../Constants.js';
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

export default {
    name: 'UserRegister',
    setup() {
        const router = useRouter()
        const name = ref('')
        const email = ref('')
        const password = ref('')
        const password_confirm = ref('')

        const handleSubmit = async() => {
            console.log("hello")
            if (password.value != password_confirm.value) {
                // Passwords do not match
                // alert('Passwords do not match!')
                toast.error('Passwords do not match!');
            }
            else {
                console.log("hi")
                try {
                    const response = await fetch(`${config.url}/api/user_register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        name: name.value,
                        email: email.value,
                        password: password.value
                    })
                })
                console.log(response);
                if (!response.ok) {
                    console.log(response);
                    // throw new Error(`${toast.error(data.error)}`);
                    toast.error(data.error);
                }
                else {
                    toast.success('Registered Successfully!',{autoClose: 2000});
                    setTimeout(() => {  router.push('/user_login'); }, 2000);
                    // route.push('/userlogin');
                }

                }
                catch (error) {
                    console.log(error)
                }

            }
        }

        return {
            name,
            email,
            password,
            password_confirm,
            handleSubmit
        }
    }

}


</script>

<style>

.container {

    height: 100%;
  width: 100%;
  /* display: flex; */
}

.blank {
    height: 75vh;
    background: rgba(76, 172, 250, 0.36);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);

}

.register {
    height: 75vh;
    background: rgba(230, 253, 253, 0.279);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);

}

.reg {
    padding-top: 7vh;
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