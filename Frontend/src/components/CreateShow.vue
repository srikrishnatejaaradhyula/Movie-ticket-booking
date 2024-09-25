<template>
    <div>
    <AdminNavBar/>
    <div class="container ">
         <div class="row align-items-center mx-0 my-3 d-flex justify-content-center">
             <div class="show col-md-6 col-12 ">
                 <div class="sho">
                     <form>
                         <h4 class="col-md-12 text-center ">Create Show</h4>
                         <div class="form-floating col-md-12  mb-3">
                             <input type="text" class="form-control" v-model="name" id="floatingInput" placeholder=" "
                                 required />
                             <label for="floatingInput">Show Name</label>
                         </div>
                        
                         <div class="row col-md-12  mb-3">
                            <div class="form-floating col-6">
                                <input type="datetime-local" class="form-control" v-model="starting_time" id="floatingInput" placeholder=" "
                                 required />
                                <label for="floatingInput">Starting Timing</label>
                            </div>
                            <div class="form-floating  col-6">
                             <input type="datetime-local" class="form-control" v-model="ending_time" id="floatingInput" placeholder=" "
                                 required />
                             <label for="floatingInput">Ending Timing</label>
                            </div>
                            
                         </div>
                         <div class="form-floating col-md-12  mb-3">
                             <input type="text" class="form-control" v-model="tag" id="floatingPassword"
                                 placeholder=" " required />
                             <label for="floatingPassword">Tag</label>
                         </div>
                         <div class="form-floating col-md-12  mb-3">
                             <input type="number" class="form-control" v-model="price" id="floatingPassword"
                                 placeholder=" " required />
                             <label for="floatingPassword">Price</label>
                         </div>
                         <!-- <div class="col-md-6">
                            
                         </div> -->
                         <div class="form-floating col-md-12   mb-3 ">
                             <input type="number" min="0" max="5"  class="form-control" v-model="rating" id="floatingInput" placeholder=" "
                                 required />
                             <label for="floatingInput">Rating</label>
                              

                             
                             
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
import { ref,reactive,computed,onMounted,onUpdated } from 'vue'
import { useRouter,useRoute } from 'vue-router'
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import VueJwtDecode from 'vue-jwt-decode'

export default {
    name: 'CreateShow',
    components: {
        AdminNavBar
    },
    setup() {
        const router = useRouter()
        const show = reactive({
            Shows: []
        });
        const name = ref('')
        const tag = ref('')
        const price = ref()
        const rating = ref()
        const starting_time = ref('')
        const ending_time = ref('')
        const route = useRoute()

        console.log(starting_time.value)
        console.log(ending_time.value)
        console.log(rating.value)

        const id = computed(() => route.params.id);
        console.log(id.value)

        const token = localStorage.getItem('isAdmin')
        const user = VueJwtDecode.decode(token)

        const handleSubmit = async() => {
            console.log(starting_time.value)
            console.log(ending_time.value)
            console.log(rating.value)

            try {
                const response = await fetch(`${config.url}/api/create_show`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-tokens': token  
                },
                body: JSON.stringify({
                    name: name.value,
                    tag: tag.value,
                    price: price.value,
                    rating: rating.value,
                    starting_time: starting_time.value,
                    ending_time: ending_time.value,
                    venue_id: id.value
                })
            })
            console.log(response);
            if (!response.ok) {
                console.log(response);
                throw new Error(`${alert(data.error)}`);
            }
            else {
                toast.success('Show Created Successfully!',{autoClose: 1000});
                setTimeout(() => {  router.push('/admin_home'); }, 1000);
            }

            }
            catch (error) {
                console.log(error)
                // alert("E-mail is already used!")
            }
        }

        const fetchShow = async () => {
            const response = await fetch(`${config.url}/api/get_show_all`, {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'x-access-tokens': token
                },
                body: JSON.stringify({
                // admin_id: user.id
                })
            });
            const data = await response.json();
            show.shows = data;
        };

        onMounted(() => {
            fetchShow();
        });
        const date = new Date();
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
            if (starting_time.value < date.toISOString().slice(0,16) && starting_time.value != '') {
                toast.warning('Starting time must be greater then current time');
                starting_time.value = '';
            }
            if(starting_time.value > ending_time.value && starting_time.value != '' && ending_time.value != ''){
                toast.warning('Starting time must be less then ending time');
                starting_time.value = '';
                ending_time.value = '';
            }
            for (let i = 0; i < show.shows.length; i++) {
                if (name.value == show.shows[i].name) {
                    toast.warning('Show name already exists');
                    name.value = '';
                }
            }
        })

        return {
            name,
            tag,
            price,
            handleSubmit,
            rating,
            starting_time,
            ending_time

        }
    }

}


</script>





 <style>

.container {
    height: 100%;
    width: 100%;
}


.show{
    height: 80vh;
    background: rgba(230, 253, 253, 0.279);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5.6px);
    -webkit-backdrop-filter: blur(5.6px);
    border: 1px solid rgba(255, 255, 255, 0.08);

}

.sho{
    padding-top: 7vh;
}

.form-floating input[type="text"],
.form-floating input[type="number"],
.form-floating input[type="datetime-local"],
.form-floating textarea {
    border: none;
    border-radius: 0;
    border-bottom: 1px solid #a9b0b7;
    background-color: rgba(255, 255, 255, 0);
}


.rate {
    float: left;
    height: 46px;
    padding: 0 10px;
}
.rate:not(:checked) > input {
    position:absolute;
    top:-9999px;
}
.rate:not(:checked) > label {
    float:right;
    width:1em;
    overflow:hidden;
    white-space:nowrap;
    cursor:pointer;
    font-size:30px;
    color:#ccc;
}
.rate:not(:checked) > label:before {
    content: '★ ';
}
.rate > input:checked ~ label {
    color: #ffc700;    
}
.rate:not(:checked) > label:hover,
.rate:not(:checked) > label:hover ~ label {
    color: #deb217;  
}
.rate > input:checked + label:hover,
.rate > input:checked + label:hover ~ label,
.rate > input:checked ~ label:hover,
.rate > input:checked ~ label:hover ~ label,
.rate > label:hover ~ input:checked ~ label {
    color: #c59b08;
}

</style>