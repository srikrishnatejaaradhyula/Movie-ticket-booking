<template>
    <div>
        <div v-for="i in star" style="display: inline;">
            <i class="bi bi-star-fill" style="color: gold"></i>
        </div>
        <div v-for="j in notRated" style="display: inline;"> 
            <i class="bi bi-star"></i>
        </div>
    </div>
</template>

<script>
import { ref, watch } from 'vue';

export default {
    name: "StarRating",
    props: ['rating'],
    setup(props) {
        const star = ref();
        const notRated = ref();
        
        const updateRating = () => {
            star.value = props.rating;
            notRated.value = 5 - props.rating;
        };
        
        // Watch for changes in the 'rating' prop and update the display accordingly
        watch(() => props.rating, updateRating);

        // Initial setup
        updateRating();

        return {
            star,
            notRated,
            updateRating
        };
    }
};
</script>