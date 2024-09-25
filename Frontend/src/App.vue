<script setup>
import router from './router';
import Landing from './components/Landing.vue';
</script>

<template>

    <router-view v-slot="{ Component, route }">
        <transition name="scale" mode="out-in">
            <component :is="Component" />
        </transition>
    </router-view>
</template>

<style scoped>
body,
html,
#app {
    width: 100%;
    height: 100%;

}

.scale-enter-active,
.scale-leave-active {
    transition: all 0.5s ease;
}

.scale-enter-from,
.scale-leave-to {
    opacity: 0;
    transform: scale(0.9);
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
    background: rgb(213, 162, 255);
    border-radius: 10px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
    background: #c64bff;
}
</style>