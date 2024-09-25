<template>
    <!-- <div> 
        <div v-for="i in 10">
            
            <div class="j">
                <p> {{ i +" " }} </p>
                <input type="checkbox" name="j" id="check" v-for="j in 10">
            </div>
        </div>

    </div> -->

    <div>
      <h1>Movie Seat Ticket Booking</h1>
      <div class="seats">
        <ul>
          <li v-for="(seat, i) in seats" :key="i">
            <input type="checkbox" :id="seat.id" v-model="seat.checked" />
            <label :for="seat.id">{{ seat.name }}</label>
            <span>{{ seat.price }}</span>
          </li>
        </ul>
      </div>
      <button @click="checkout">Checkout</button>
    </div>
</template>

<script>
import { ref } from 'vue';

export default {
    name: 'Sample',
    setup(){
        


        return {
            
        }
    }
}
</script>

<style>
.j p { 
    display: inline; 
}
</style>


