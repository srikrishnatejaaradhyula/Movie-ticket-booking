<template>
    <div  class="show card w-100 my-4 " v-for="s in show.shows" :key="s.id" >
        <div class="card-header">
            <div class="d-flex justify-content-between">
                <div class="d-flex">
                    <h3>{{ s.name }}</h3> 
                    <h5 class="text-bottom"> &nbsp;&nbsp; {{ s.tag }}</h5>
                </div>
                <div class="d-flex" >
                    <button type="button" class="btn btn-outline h-auto dropdown-toggle dropdown-toggle-split"
                        data-bs-toggle="dropdown" aria-expanded="false">
                    </button>
                    <ul class="dropdown-menu h-auto w-auto">
                        <li style="background-color: rgb(162, 177, 255);">
                            <router-link  class="dropdown-item" :to="/update_show/ + s.id ">Edit</router-link>
                        </li>
                        <li style="background-color: rgb(253, 135, 135);">
                            <button  class="dropdown-item" @click.prevent="DeleteShow(s.id)">Delete</button>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="card-body w-auto" >
                <!-- {{ s.starting_time }} -
                {{ s.ending_time }} -->
                {{ s.common_date }} <br>
                {{ s.time_range }} <br>
                Price : {{ s.price }} <br>
                <!-- Rating : {{ s.rating }} <br> -->
                <StarRating :rating="s.rating"  />
        </div>
        <!-- <div class="card-body w-auto" v-else>
                {{ s.starting_time }} -
                {{ s.ending_time }}
                <center><h5>
                {{ s.common_date }} <br>
                {{ s.time_range }} <br>
                Price : {{ s.price }}  Rating : {{ s.rating }} <br> 
                </h5>
                <button class=" primary-button w-auto"  @click="$router.push('/booking_show/' + s.id)">Book Show</button></center>
        </div> -->

    </div>
</template>

<script>
import {config} from '../Constants.js';
import StarRating from './StarRating.vue';
import { ref, onMounted, reactive } from "vue";
import VueJwtDecode from 'vue-jwt-decode'
import { toast } from 'vue3-toastify';

export default {
    name: "AdminGetShow",
    components: {
        StarRating
    },
    props: {
        id: {
            type: Number,
            required: true
        }
    },
    setup(props) {
        const show = reactive({
            shows: []
        });
        const edit = props.edit
        const token = localStorage.getItem('isAdmin')
        const user = VueJwtDecode.decode(token)

        const fetchShow = async () => {
            const response = await fetch(`${config.url}/api/get_show`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': token
                },
                body: JSON.stringify({
                    venue_id: props.id
                })
            });
            const data = await response.json()
            show.shows = data
            console.log(show.shows)
        }


        onMounted(() => {
            fetchShow()
        });

        const DeleteShow = async (id) => {
            const response = await fetch(`${config.url}/api/delete_show`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': token
                },
                body: JSON.stringify({
                    show_id: id
                })
            });
            const data = await response.json()
            console.log(data)
            if (response.status === 200) {
                toast.success('Show Deleted Successfully');
                // Fetch fresh data after successful deletion
                fetchShow();
            }
            else if (response.status === 400) {
                toast.error(data.error); 
            }else {
                alert("Something went wrong");
            }
        }

        
 
        const SplitDate = (stating,ending) => {
            const start = stating.slice(0,10);
            const end = ending.slice(0,10);

        }
        return {
            show,
            DeleteShow,
        }

    }
}

</script>

<style scoped>

.show {
    background-color: rgba(192, 213, 114, 0.251);
    border-radius: 10px;
    box-shadow: 0px 0px 10px 0px rgba(21, 46, 22, 0.393);
    width: 100%;
}
</style>
