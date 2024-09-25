<template>
    <div>
        <UserNavBar/>
        <div class="container">
            <div class="row" v-for="b in booking.bookings" :key="b.id">
                <div class="col-md-12">
                    <div class="booking-card card my-2">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-lg-10 col-md-8 col-7" style="display:inline">
                                    <h5  style="display:inline">
                                        <span  style="color: brown;">{{ b.venue_name}}</span><hr >
                                        <span  style="color: rgb(165, 61, 42);">{{ b.show_name}} &nbsp</span> 
                                        <span  style="color: rgb(165, 126, 42);">{{ b.show_date}} &nbsp&nbsp</span>
                                        <span  style="color: rgb(42, 165, 89);">Show Time: {{ b.show_time}}&nbsp&nbsp </span>
                                        <span  style="color: rgb(42, 118, 165);">No. Of Seats: {{ b.seats_booked}} &nbsp&nbsp</span> 
                                        <span  style="color: rgb(132, 42, 165);">Total Paid: {{ b.total_price }} &nbsp&nbsp</span> 
                                        <span  style="color: rgb(163, 139, 20);"><StarRating :rating="b.rating" style="display:inline" /></span>
                                        
                                    </h5>
                                   
                                </div>
                                <div class="col-lg-2 col-md-4 col-5 d-flex justify-content-end "  style="display:inline">


                                 <button type="button"   @click="openModal(b.id)" class="primary-button" style="height: min-content;">Give Rating</button>
                                        
                                        <Teleport to="#modal">
                                            <div class="modal-bg" v-if="IsModalOpen">

                                                <!-- <BookingRating :id="b.id" v-model="IsModalOpen"/> -->

                                                  <div class="container h-auto w-auto  p-5" style="background-color: antiquewhite; border-radius: 10px;">
                                                    <h4>Please proved rating </h4>
                                                    <div class="form-floating col-md-12  mb-3">
                                                        <input type="number" class="form-control" v-model="rating"  id="floatingPassword"
                                                            placeholder=" "   />
                                                        <label for="floatingPassword">rating</label>
                                                    </div>
                                                    
                                                    <div class="container d-flex justify-content-center align-center">
                                                        <div class="row d-flex justify-content-evenly">
                                                            <div class="col text-center " >
                                                                <button type="button"  @click="update(currentBookingId,rating)"  class="btn btn-success " >
                                                                    conform!
                                                                </button>
                                                            </div>
                                                            <div class="col text-center ">
                                                                <button type="button" @click="IsModalOpen = false"  class="btn btn-danger">Cancel</button>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>

                                            </div>
                                        </Teleport>
                                </div >
                            </div>  

                        </div>
                    </div>
                    
                    
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import UserNavBar from './UserNavBar.vue';
import StarRating from './StarRating.vue';
import {config} from '../Constants.js';
import { ref, onMounted,reactive,onUpdated} from "vue";
import VueJwtDecode from 'vue-jwt-decode'
import { toast } from 'vue3-toastify';

export default {
    name: "UserBookings",
    components : {
        UserNavBar,
        StarRating 
    },
    setup() {
        const booking = reactive({
            bookings: []
        });
        const rating = ref();
        const currentBookingId = ref(null);
        // const renderComponent = ref(true);

        const openModal = (bookingId) => {
            currentBookingId.value = bookingId;
            IsModalOpen.value = true;
        };

        const IsModalOpen = ref(false);
        const token = localStorage.getItem('token')
        const user = VueJwtDecode.decode(token)
      

        const fetchBookingData = async () => {
            const response = await fetch(`${config.url}/api/get_user_booking`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'x-access-tokens': token
                },
                body: JSON.stringify({
                user_id: user.id
                })
            });
            const data = await response.json();
            booking.bookings = data;
            console.log(booking.bookings);
        };
        // Fetch venue data on initial mount
        onMounted(fetchBookingData);


        const update = async (id,rate) => {
            const response = await fetch(`${config.url}/api/update_rating`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'x-access-tokens': token
                },
                body: JSON.stringify({
                    booking_id: id,
                    rating: rate
                })
            });
            const data = await response.json();
            if (response.status === 200) {
                // toast.success('Rating updated successfully');
                toast.success('Rating updated  Successfully!',{autoClose: 1000});
                IsModalOpen.value = false;
                rating.value = 0;
                console.log("booking id :",id);
                console.log("rating :",rate);
                fetchBookingData();
               
            } else {
                toast.error('Rating update failed');
            }
        }

        onUpdated(() => {
            if (rating.value > 5) {
                toast.warning('Rating must be less then 5');
                rating.value = 5;
            }
            if (rating.value < 0) {
                toast.warning('Rating must be greater then 0');
                rating.value = 0;
            }
            if (rating.value%1 != 0 && rating.value != null) {
                toast.warning('Rating must be an integer');
                rating.value = rating.value - rating.value%1 ;
            }
        })

        return {
            booking,
            IsModalOpen,
            rating,
            update,
            currentBookingId,
            openModal,
            // renderComponent
        }
    }

}

</script>

<style scoped>
.booking-card{
    background: rgba(182, 249, 254, 0.226);
    /* backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px); */
    border-radius: 10px;
    box-shadow: 0px 0px 10px 0px rgba(21, 34, 46, 0.683);
    width: auto;
}
.modal-bg{
    background-color: rgba(0, 0, 0, 0.224);
}
</style>