<template>
    <div class="container forgetpassword">
        <div class="row align-items-center my-auto" > 
            <div class="col" v-if="!isOtpSent && !verified">
                <h5>Enter Your register Email</h5>
                <div class="form-floating col-md-12">
                    <input type="email" class="form-control" v-model="email"  id="floatingPassword"
                        placeholder=" "   />
                    <label for="floatingPassword">Email</label>
                </div>
                <div class="col-md-12 my-4 d-flex justify-content-center" v-if="!sending">
                    <button @click="sendOtp" class="primary-button"> Send Otp</button>
                </div>

                <div class="col-md-12 my-4 d-flex justify-content-center" v-else>
                    <div class="spinner-grow text-success" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="spinner-grow text-success" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="spinner-grow text-success" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>

            </div>
            <div v-else-if="isOtpSent && !verified">
                <h5>Enter Otp</h5>
                <div class="form-floating col-md-12">
                    <input type="number" class="form-control" v-model="user_otp"  id="floatingPassword"
                        placeholder=" "   />
                    <label for="floatingPassword">Otp</label>
                </div>
                <div class="col-md-12 my-4 d-flex justify-content-center">
                    <button @click="verifyOtp" class="primary-button"> Verify Otp</button>
                </div>
            </div>
            <div v-else>
                <h5>Enter New Password</h5>
                <div class="form-floating col-md-12">
                    <input type="password" class="form-control" v-model="password"  id="floatingPassword"
                        placeholder=" "   />
                    <label for="floatingPassword">Password</label>
                </div>
                <div class="form-floating col-md-12">
                    <input type="password" class="form-control" v-model="confirm_password"  id="floatingPassword"
                        placeholder=" "   />
                    <label for="floatingPassword">Confirm Password</label>
                </div>
                <div class="col-md-12 my-4 d-flex justify-content-center">
                    <button @click="changePassword" class="primary-button"> Change Password</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { f } from 'awesome-vue-star-rating';
import {config} from '../Constants.js';
import { ref,reactive,onMounted,computed,onUpdated } from 'vue'
import { useRouter,useRoute } from 'vue-router'
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';


export default {
    name: "ForgotPassword",
    setup() {
        const email = ref();
        const router = useRouter()
        const route = useRoute()
        const otp = ref();
        const user_otp = ref();
        const password = ref();
        const confirm_password = ref();
        const isOtpSent = ref(false);
        const verified = ref(false);
        const sending = ref(false);
        // otp.value = Math.floor(100000 + Math.random() * 900000);
        const sendOtp = async() => {
            sending.value = true;
            const response = await fetch(`${config.url}/api/send_otp`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email.value
                })
            });
            const data = await response.json();
            otp.value = data.otp;
            console.log(data);
            if(response.status === 200){
                sending.value = false;
                toast.success("Otp was send to your email");
                isOtpSent.value = true;
            }
            else{
                sending.value = false;
                toast.error(data.message);
            }
        }
        const verifyOtp = () => {
            if(otp.value == user_otp.value){
                toast.success("Otp was verified");
                verified.value = true;
            }
            else{
                toast.error(data.message);
            }
        }
        const changePassword = async() => {
            if(password.value == confirm_password.value){
                const response = await fetch(`${config.url}/api/change_password`, {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email.value,
                        password: password.value
                    })
                });
                const data = await response.json();
                console.log(data);
                if(response.status === 200){
                    toast.success("Password was changed");
                    setTimeout(() => {  router.push('/user_login'); }, 1000);
                }
                else{
                    toast.error(data.message);
                }
            }
            else{
                toast.error("Password and confirm password should be same");
            }
        }
        return{
            email,
            sendOtp,
            isOtpSent,
            user_otp,
            verifyOtp,
            verified,
            changePassword,
            password,
            confirm_password,
            sending
            
        }
    }
}
</script>

<style>
.forgetpassword{
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>