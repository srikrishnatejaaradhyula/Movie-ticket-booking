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
                                <router-link to="/admin_home" class="nav-link">
                                    <i class="bi bi-house"></i> Home
                                </router-link>
                            </li>
                            <li class="nav-item px-3">
                                <router-link to="/admin_summery" class="nav-link">
                                    <i class="bi bi-bar-chart-line"></i> Summery
                                </router-link>
                            </li>
                            <li class="nav-item dropdown ">
                                <a class="nav-link dropdown-toggle h-auto align-middle" href="#" role="button"
                                    data-bs-toggle="dropdown" aria-expanded="false">

                                    <p class="text-end align-top ms-2 fw-bolder" style="display: inline">
                                        {{ username }}
                                    </p>
                                </a>
                                <ul class="dropdown-menu h-auto">
                                    
                                    <li>
                                        <button class="dropdown-item btn btn-outline-light" @click="export_csv()"
                                            style="color: rgb(85, 160, 103) ;">
                                            <i class="bi bi-download"></i> export csv
                                        </button>
                                    </li>
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
import {csvParser} from '../csv-parser.js'
import {config} from '../Constants.js';
import { useRouter } from 'vue-router'
import { ref, onMounted,reactive } from 'vue'
import VueJwtDecode from 'vue-jwt-decode'


export default {
    name: "AdminNavBar",
    setup() {
        const username = ref('')

        const show = reactive({
            shows: []
        });
        

        const token = localStorage.getItem('isAdmin')
        const user = VueJwtDecode.decode(token)

        username.value = user.name
        console.log(username.value)
        const router = useRouter()
        const logout = () => {
            localStorage.removeItem('isAdmin');

            router.push('/')
        }
        const export_csv = async() =>{
            const response = await fetch(`${config.url}/api/get_show_all`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': token
                },
            });
            const data = await response.json()
            show.shows = data
            if (response.status !== 200) {
                throw new Error(data.message)
            }
            csvParser().exportDataFromJSON(show.shows, null, null);
        }
        return {
            logout,
            username,
            export_csv

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