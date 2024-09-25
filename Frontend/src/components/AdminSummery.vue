<template>
    <div class="overflow-x-hidden">
        <AdminNavBar/>
        <div class="container" >
                <div  class="col-md-12" v-for="v in venue.venues" :id="v.revenue "> 
                    <SummeryLineChart 
                        :title="'Revenue'" 
                        :data="v.revenue"
                        :labels="v.venue_name"
                    />
                </div>
            <div class="row"  v-for="s in show.shows" :id="s.id">
                
                <div class="col-md-12">
                    <h4 class="col-md-12 text-center ">{{ s.name }}</h4>
                </div>
                <div class="col-md-6">
                    <SummeryBarChart 
                        :title="'ratings'" 
                        :data="[s.user_rating, s.admin_rating,0]"
                        :labels="['User Rating', 'Admin Rating']"
                        :color="['#FFC107', '#3F51B5']"
                    />
                </div>
                <div class="col-md-6">
                    <SummeryBarChart 
                        :title="'booking'" 
                        :data="[s.booking_count, s.Unoccupied_seats,0]"
                        :labels="['Booked Seats', 'Unoccupied Seats']"
                        :color="['#99ff99', '#ff6666']"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AdminNavBar from './AdminNavBar.vue';
import SummeryBarChart from './SummeryBarChart.vue';
import SummeryLineChart from './SummeryLineChart.vue';
import {config} from '../Constants.js';
import { ref,reactive,onMounted,computed,onUpdated } from 'vue'
import { useRouter,useRoute } from 'vue-router'
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
// import VueJwtDecode from 'vue-jwt-decode';

export default {
    name:"AdminSummery",
    components: {
        AdminNavBar,
        SummeryBarChart,
        SummeryLineChart
    },
    setup(){
        const router = useRouter()
        const show = reactive({
            shows: []
        });
        const venue = reactive({
            venues: []
        });

        const token = localStorage.getItem('isAdmin')
        // const user = VueJwtDecode.decode(token)
        console.log(token)

        const fetchShow = async () => {
            const response = await fetch(`${config.url}/api/get_show_for_summery`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'x-access-tokens': token
                }
            });
            const data = await response.json();
            show.shows = data;
            
        }

        const fetchVenue = async () => {
            const response = await fetch(`${config.url}/api/get_venue_for_summery`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'x-access-tokens': token
                }
            });
            const data = await response.json();
            venue.venues = data;
            console.log(venue.venues.reverse)
            venue.venues.forEach((v) => {
                console.log(v.revenue)
            });
        }

        onMounted(() => {
            fetchShow();
            fetchVenue();
        });
        
        
        return {
            show,
            venue
        }
    }
}
</script>