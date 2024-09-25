<template>
    <div>
    <UserNavBar/>
    <div class="container">
         <div class="row align-items-center mx-0 my-5 d-flex justify-content-center">
             <div class="venue col-md-6 col-12 ">
                 <div class="ven">
                     <form>
                        <h4 class="col-md-12 text-center ">Booking Show</h4>
                        <div class="form-floating col-md-12  mb-3">
                             <!-- <input type="text" class="form-control" v-model="name" id="floatingInput" placeholder=" "
                                 required />
                             <label for="floatingInput">Venue Name</label> -->
                            <h5>Available Seats : {{ show.shows.available_seats }}</h5> 
                        </div> 
                        <div class="form-floating col-md-12  mb-3">
                             <input type="number" class="form-control" v-model="number" id="floatingInput" placeholder=" "
                                required />
                             <label for="floatingInput">Number of Seats</label>
                        </div>
                        <div class="form-floating col-md-12  mb-3">
                             <input type="number" class="form-control" v-model="price" id="floatingPassword"
                                 placeholder=" " readonly />
                             <label for="floatingPassword">Price Per Ticket</label>
                        </div>
                        <div class="form-floating col-md-12  mb-3">
                             <input type="number" class="form-control" v-model="total" id="floatingPassword"
                                 placeholder=" " readonly />
                             <label for="floatingPassword">Total price</label>
                        </div>
                        <div class="col-md-12 text-center pt-1">
                             <button type="button" @click="IsModalOpen = true"  class="primary-button">Book</button>

                            <Teleport to="#modal">
                                <!-- <h2>hello world</h2> -->
                                <div class="modal-bg" v-if="IsModalOpen">
                                    <div class="container h-auto w-auto  p-5" style="background-color: antiquewhite; border-radius: 10px;">
                                        <h5 class="text-center">Are you sure you want to book?</h5>
                                        <!-- <button class="close" @click="IsModalOpen = false">X</button> -->
                                        
                                        <div class="container d-flex justify-content-center align-center">
                                            <div class="row d-flex justify-content-evenly" v-if="!isBooking">
                                                <div class="col text-center " >
                                                    <button type="button" @click="bookShow"  class="btn btn-success " >
                                                        conform!
                                                    </button>
                                                    <!-- <span v-if="isBooking">
                                                        <SquareSpinner size="20" color="#ffffff" />
                                                    </span> -->
                                                </div>
                                                <div class="col text-center ">
                                                    <button type="button" @click="IsModalOpen = false"  class="btn btn-danger">Cancel</button>
                                                </div>
                                            </div>
                                            <div v-else>
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
                                    </div>
                                </div>
                            </Teleport>

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
import UserNavBar from '@/components/UserNavBar.vue'
import { ref,reactive,onMounted,computed,onUpdated } from 'vue'
import { useRouter,useRoute } from 'vue-router'
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import VueJwtDecode from 'vue-jwt-decode';

export default {
    name:"BookingShow",
    components: {
        UserNavBar,
    },
    setup(){
        const router = useRouter()
        const route = useRoute()
        const show = reactive({
            shows: []
        });
        const number = ref()
        const price = ref()
        const total = ref()
        const isBooking = ref(false);
        const id = computed(() => route.params.id);
        console.log(id.value)
        
        const IsModalOpen = ref(false)

        const token = localStorage.getItem('token')
        const user = VueJwtDecode.decode(token)
        console.log(token)

        const fetchShow = async () => {
            const response = await fetch(`${config.url}/api/get_show_by_id`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': token
                },
                body: JSON.stringify({
                    show_id: id.value
                })
            });
            const data = await response.json()
            show.shows = data
            console.log(show.shows)
            price.value = show.shows.price
            total.value = price.value * number.value

        }


        const bookShow = async () => {
            isBooking.value = true; 
            const response = await fetch(`${config.url}/api/book_show`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': token
                },
                body: JSON.stringify({
                    show_id: id.value,
                    seats: number.value,
                    price_per_ticket: price.value,
                    total_price: total.value,
                    user_id: user.id
                })
            });
            const data = await response.json()
            console.log(data)
            if(response.status === 200){
                isBooking.value = false;
                IsModalOpen.value = false
                // toast.success("booked successfully")
                // router.push('/user_home')
                toast.success('Ticket booked Successfully!',{autoClose: 1000});
                setTimeout(() => {  router.push('/user_home'); }, 1000);
            }
            else{
                isBooking.value = false; 
                toast.error(data.message)
            }
        }

        onMounted(() => {
            fetchShow()
        })

        onUpdated(() => {
            total.value = price.value * number.value
            if (number.value > show.shows.available_seats) {
                toast.warning("Number of seats should be less than available seats")
                number.value = 0
                total.value = 0
            }
            if(number.value < 0){
                toast.warning("Number of seats should be greater than 0")
                number.value = 0
                total.value = 0
            }
        })

        return{
            number,
            price,
            total,
            IsModalOpen,
            show,
            bookShow,
            isBooking,
        }
    }
}

</script>