<template>
    <div>
        <UserNavBar />
        <div class="d-flex justify-content-center my-2" >
            <input type="search" v-model="search" placeholder="Search" class="form-control" style="width: min-content;">
        </div>
        <div class="d-flex justify-content-center my-2" style="display: inline;" >
            <div class="px-2">
                <input type="date" v-model="search" class="form-control" style="width: min-content;">
            </div>
            <div >
                <button class="btn btn-primary" @click="search = ''"> Clear Date</button>
            </div>
        </div>
        <div class="container">
            <div class=" venueContainer row venue my-4 mx-1 h-auto" v-for="v in filterVenue" :key="v.id" >
            <h2 style="color:brown">{{ v.name }}</h2>
            <h6>Address : {{ v.place }},{{ v.location }}</h6>
                <div class="col-lg-3 col-md-4 col-sm-6 col-12" v-for="s in v.shows" :key="s.id">
                    <!-- <UserGetShow :id="v.id" :search="search"/> -->
                   
                        <div class="usershows card w-100 my-4"  v-if="v.id == s.venue_id " >
                            <div >
                                <div class="card-header">
                                    <div class="d-flex justify-content-between">
                                        <div class="d-flex">
                                            <h3>{{ s.name }}</h3> 
                                            <h5 class="text-bottom"> &nbsp;&nbsp; {{ s.tag }}</h5>
                                        </div>
                                    </div>
                                </div>

                                <div class="card-body w-auto" >
                                    <center>
                                        <h5>
                                            {{ s.common_date }} <br>
                                            {{ s.time_range }} <br>
                                            Price : {{ s.price }} 
                                             <!-- Rating : {{ s.rating }}  <br>  -->
                                             <StarRating :rating="s.rating"  />
                                        </h5>
                                        <div v-if="s.available_seats > 0 && s.viewable">
                                            <button class=" primary-button w-auto"  @click="$router.push('/booking_show/' + s.id)">Book Show</button>
                                        </div>
                                        <div v-else-if="!s.viewable">
                                            <button class=" primary-button w-auto" disabled>Show was Completed</button>
                                            
                                        </div>
                                        <div v-else>
                                            <button class=" primary-button w-auto" disabled>Housefull</button>
                                        </div>
                                    </center>
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
import UserNavBar from './UserNavBar.vue'
import StarRating from './StarRating.vue'
import { ref, onMounted, reactive,computed} from "vue";
import VueJwtDecode from 'vue-jwt-decode'
import { toast } from 'vue3-toastify';
import { useRouter } from 'vue-router';
import { f } from 'awesome-vue-star-rating';


export default {
    name: "UserHome",
    components: {
        UserNavBar,
        StarRating
    },
    setup() {

        const venue = reactive({
            venues: []
        });
        const show = reactive({ 
            shows: []
        });
        
        const search = ref("");
        const searchdate = ref("");

        const router = useRouter()
        const token = localStorage.getItem('token')
        const user = VueJwtDecode.decode(token)
        
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
            venue.venues.forEach((v) => {
                v.shows = [];
            });
            console.log(venue.venues);

            const response1 = await fetch(`${config.url}/api/get_show_all`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'x-access-tokens': token
                },
                body: JSON.stringify({
                // admin_id: user.id
                })
            });
            const data1 = await response1.json();
            show.shows = data1;
            venue.venues.forEach((v) => {
                show.shows.forEach((s) => {
                    if (v.id == s.venue_id) {
                        v.shows.push(s);
                    }
                });
            });
            console.log(venue.venues);
            };



        // Fetch venue data on initial mount
        onMounted(fetchVenueData);


        const formatDate = (dateString) => {
            const options = { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' };
            const date = new Date(dateString);
            const formattedDate = date.toLocaleDateString('en-US', options);
            const formatDate = formattedDate.replace(/,/g, '');
            const [weekday, month, day, year] = formatDate.split(' ');

            return `${weekday}, ${day} ${month} ${year}`;
        };

        const filterVenue = computed(() => {
                return venue.venues.filter((v) => {
                    const nameMatch = v.name.toLowerCase().includes(search.value.toLowerCase());
                    const placeMatch = v.place.toLowerCase().includes(search.value.toLowerCase());
                    const locationMatch = v.location.toLowerCase().includes(search.value.toLowerCase());
                    const showMatch = v.shows.some((s) => s.name.toLowerCase().includes(search.value.toLowerCase()));
                    const tagMatch = v.shows.some((s) => s.tag.toLowerCase().includes(search.value.toLowerCase()));
                    const ratingMatch = v.shows.some((s) => s.rating.toString().includes(search.value.toString()));
                    const dateMatch = v.shows.some((s) =>s.common_date.toString().includes(formatDate(search.value).toString()));
                    // const dateMatch = v.shows.some((s) => {
                    //     const showDate = new Date(s.common_date).setHours(0, 0, 0, 0);
                    //     const searchDate = new Date(searchdate.value).setHours(0, 0, 0, 0);

                    //     return showDate === searchDate;
                    // });
                    console.log(nameMatch);
                    console.log(dateMatch);
                    return  nameMatch || showMatch || tagMatch || placeMatch || locationMatch || ratingMatch || dateMatch;
                });
        });

        



        return {
            venue,
            filterVenue,
            search,
            searchdate
            // show
        }
    }
}
</script>

<style scoped>

.venueContainer{
    background: rgba(182, 249, 254, 0.226);
    /* backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px); */
    border-radius: 10px;
    box-shadow: 0px 0px 10px 0px rgba(21, 34, 46, 0.683);
    width: auto;
}
.usershows {
    background-color: rgba(192, 213, 114, 0.251);
    border-radius: 10px;
    box-shadow: 0px 0px 10px 0px rgba(21, 46, 22, 0.393); 
}
</style>