<template>
    <div class="overflow-y-hidden" >
        <AdminNavBar />
            <!-- Add New venue Button -->
        <div class="d-grid gap-2 d-md-flex justify-content-md-end d-grid gap-2 w-auto" >
            <button class=" primary-button m-2" @click="$router.push('/create_venue')">Add Venue</button>
        </div>

        <div class="container-fluid">
            <div class="row">
                <div class="card_style col-lg-4 col-sm-6 col-12 my-5 d-flex justify-content-evenly" v-for="v in venue.venues" :key="v.id" >
                    <!-- venue -->
 
                    <div class="card " >
                        <div class="card-header">
                            <div class="d-flex justify-content-between">
                                <div class="d-flex">
                                    <h3>{{ v.name }}</h3>
                                </div>
                                <div class="d-flex dropstart">
                                    <button type="button" class="btn btn-outline h-auto dropdown-toggle dropdown-toggle-split"
                                        data-bs-toggle="dropdown" aria-expanded="false">
                                    </button>
                                    <ul class="dropdown-menu h-auto ">
                                        <li style="background-color: rgb(162, 177, 255);">
                                            <router-link class="dropdown-item" :to="/update_venue/ + v.id">Edit</router-link>
                                        </li >
                                        <li style="background-color: rgb(255, 162, 162);">
                                            <button class="dropdown-item" @click.prevent="DeleteVenue(v.id)">Delete</button>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div class="card-body overflow-auto h-auto" >
                            <h5>Address : {{ v.place }},{{ v.location }}</h5>
                            <h5>Capacity : {{ v.capacity }}</h5>
                        </div>
                        <div class="card-body overflow-auto" style="height: 55vh;" >
                            
                            <AdminGetShow :id="v.id" />

                        </div>


                        <!-- footer -->

                        <div class="card-footer">
                            <div class="d-flex justify-content-around">
                                
                                    <button class=" primary-button w-auto"  @click="$router.push('/create_show/' + v.id)">Add Show</button>
                                
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

</template>

<script>
import {config} from '../Constants.js';
import AdminNavBar from './AdminNavBar.vue'
import AdminGetShow from './AdminGetShow.vue';
import { ref, onMounted, reactive,getCurrentInstance } from "vue";
import VueJwtDecode from 'vue-jwt-decode'
import { toast } from 'vue3-toastify';
import { useRouter } from 'vue-router';

export default {
    name: "AdminHome",
    components: {
        AdminNavBar,
        AdminGetShow
    },
    setup() {

        const venue = reactive({
            venues: []
        });
        // const show = reactive({
        //     shows: []
        // });

        const router = useRouter()
        const token = localStorage.getItem('isAdmin')
        const user = VueJwtDecode.decode(token)

                    // Function to fetch venue data
        const fetchVenueData = async () => {
            const response = await fetch(`${config.url}/api/get_venue`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'x-access-tokens': token
                },
                body: JSON.stringify({
                admin_id: user.id
                })
            });
            const data = await response.json();
            venue.venues = data;
            console.log(venue.venues[0].id);
            console.log(venue.venues)
        };

        // Fetch venue data on initial mount
        onMounted(fetchVenueData);

        // Function to delete a venue
        const DeleteVenue = async (id) => {
            const response = await fetch(`${config.url}/api/delete_venue`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'x-access-tokens': token
                },
                body: JSON.stringify({
                venue_id: id
                })
            });
            const data = await response.json();
            console.log(data);
            if (response.status === 200) {
                toast.success('Venue Deleted Successfully');
                // Fetch fresh data after successful deletion
                fetchVenueData();
            } else {
                alert("Something went wrong");
            }
        };


        
        return {
            venue,
            user,
            fetchVenueData,
            DeleteVenue
        }
    }
}
</script>

<style scoped>
.card {
    background: rgba(182, 249, 254, 0.226);
    /* backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px); */
    border-radius: 10px;
    box-shadow: 0px 0px 10px 0px rgba(21, 34, 46, 0.683);
    width: 30vw;
}

.card:hover {
    width: 78vh;
}

.primary-button{
    padding: 0.5% 1.5%;
}
    /* width */
    ::-webkit-scrollbar {
        width: 10px;
    }

    /* Track */
    ::-webkit-scrollbar-track {
        box-shadow: inset 0 0 5px rgba(253, 253, 253, 0.219); 
        border-radius: 10px;
    }

    /* Handle */
    ::-webkit-scrollbar-thumb {
        background: #8fb0ff;
        border-radius: 10px;
    }

    /* Handle on hover */
    ::-webkit-scrollbar-thumb:hover {
        background: #8fb0ff;
    }
</style>