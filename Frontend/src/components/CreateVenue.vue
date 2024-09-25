<template>
    <div>
    <AdminNavBar/>
    <div class="container">
         <div class="row align-items-center mx-0 my-5 d-flex justify-content-center">
             <div class="venue col-md-6 col-12 ">
                 <div class="ven">
                     <form>
                         <h4 class="col-md-12 text-center ">Create Venue</h4>
                         <div class="form-floating col-md-12  mb-3">
                             <input type="text" class="form-control" v-model="name" id="floatingInput" placeholder=" "
                                 required />
                             <label for="floatingInput">Venue Name</label>
                         </div>
                         <div class="form-floating col-md-12  mb-3">
                             <input type="text" class="form-control" v-model="place" id="floatingInput" placeholder=" "
                                 required />
                             <label for="floatingInput">Place</label>
                         </div>
                         <div class="form-floating col-md-12  mb-3">
                             <input type="text" class="form-control" v-model="location" id="floatingPassword"
                                 placeholder=" " required />
                             <label for="floatingPassword">Loccation</label>
                         </div>
                         <div class="form-floating col-md-12  mb-3">
                             <input type="number" class="form-control" v-model="capacity" id="floatingPassword"
                                 placeholder=" " required />
                             <label for="floatingPassword">Capacity</label>
                         </div>
                         <div class="col-md-12 text-center pt-1">
                             <button type="submit" @click.prevent="handleSubmit" id="butt" class="primary-button">Create</button>
                         </div>
                     </form>
                 </div>
             </div>
         </div>
     </div>
    </div>
</template>

<script>
import {config} from '../Constants.js';
import AdminNavBar from '@/components/AdminNavBar.vue'
import { ref,reactive,onMounted,onUpdated} from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import VueJwtDecode from 'vue-jwt-decode';

export default {
    name: 'CreateVenue',
    components: {
        AdminNavBar
    },
    setup() {
        const router = useRouter()
        const venue = reactive({
            venues: []
        });
        const name = ref('')
        const place = ref('')
        const location = ref('')
        const capacity = ref()

        const token = localStorage.getItem('isAdmin');
        const user = VueJwtDecode.decode(token);

        console.log(user)

        const handleSubmit = async() => {
           
            try {
                const response = await fetch(`${config.url}/api/create_venue`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': token            //localStorage.getItem('token')
                },
                body: JSON.stringify({
                    name: name.value,
                    place: place.value,
                    location: location.value,
                    capacity: capacity.value,
                    admin_id: user.id
                })
            })
            console.log(response);
            if (!response.ok) {
                toast.error(data.error);
            }
            else {
                toast.success('Venue Created Successfully!',{autoClose: 2000});
                    setTimeout(() => {  router.push('/admin_home'); }, 2000);
            }

            }
            catch (error) {
                console.log(error)
            }
        }

        const fetchVenueData = async () => {
            const response = await fetch(`${config.url}/api/get_all_venue`, {
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
        };
        onMounted(() => {
            fetchVenueData()
        });

        onUpdated(() => {
            for (let i = 0; i < venue.venues.length; i++) {
                if (venue.venues[i].name == name.value) {
                    toast.warning('Venue Already Exists!');
                    name.value = '';
                }
            }
        });
        return {
            name,
            place,
            location,
            capacity,
            handleSubmit
        }
    }

}


</script>





 <style>

.container {
    height: 100%;
    width: 100%;
}


.venue {
    height: 75vh;
    background: rgba(230, 253, 253, 0.279);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);

}

.ven {
    padding-top: 7vh;
}

.form-floating input[type="text"],
.form-floating input[type="number"],
.form-floating input[type="password"],
.form-floating textarea {
    border: none;
    border-radius: 0;
    border-bottom: 1px solid #a9b0b7;
    background-color: rgba(255, 255, 255, 0);
}

</style>