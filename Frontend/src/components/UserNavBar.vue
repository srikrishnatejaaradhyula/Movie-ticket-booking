<template>
    <div >
        <header>
            <nav class="navbar navbar-expand-lg">
                <div class="container-fluid px-4">
                    <a class="navbar-brand animate-charcter" href="#">Ticket Show</a>

                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                        data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                        aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse h-auto" id="navbarSupportedContent">
                        <ul class="navbar-nav  ms-auto ps-auto">
                            <li class="nav-item px-3">
                                <router-link to="/user_home" class="nav-link">
                                    <i class="bi bi-house"></i> Home
                                </router-link>
                            </li>
                            <li class="nav-item px-3">
                                <router-link to="/user_bookings" class="nav-link">
                                    <i class="bi bi-calendar-event"></i> Booking
                                </router-link>
                            </li>
                            <li class="nav-item dropdown ">
                                <a class="nav-link dropdown-toggle h-auto align-middle" href="#" role="button"
                                    data-bs-toggle="dropdown" aria-expanded="false">

                                    <p class="text-end align-middle ms-2 fw-bolder" style="display: inline">
                                        {{ username }}
                                    </p>
                                </a>
                                <ul class="dropdown-menu h-auto">
                                    <li>
                                        <button class="dropdown-item btn btn-outline-light" @click="logout()"
                                            style="color: red ;">
                                            <i class="bi bi-box-arrow-left"></i> Logout
                                        </button>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
    </div>
</template>    

<script>
import {config} from '../Constants.js';
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import VueJwtDecode from 'vue-jwt-decode'


export default {
    name: "UserNavBar",
    setup() {
        const username = ref('')

        const token = localStorage.getItem('token')
        const user = VueJwtDecode.decode(token)

        username.value = user.name
        console.log(username.value)
        const router = useRouter()
        const logout = () => {
            localStorage.removeItem('token');

            router.push('/')
        }
        return {
            logout,
            username
            // user

        }
    }

};

</script>

<style scoped>

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
    font-size: 25px;
    font-weight: 600;
}

@keyframes textclip {
    to {
        background-position: 200% center;
    }
}
</style>