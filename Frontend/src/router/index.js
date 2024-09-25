import { createRouter, createWebHistory } from 'vue-router'
import Landing from "../components/Landing.vue";
import UserLogin from "../components/UserLogin.vue";
import UserRegister from "../components/UserRegister.vue";
import AdminLogin from "../components/AdminLogin.vue";
import AdminHome from "../components/AdminHome.vue";
import AdminSummery from '../components/AdminSummery.vue';
import CreateVenue from "../components/CreateVenue.vue";
import UpdateVenue from "../components/UpdateVenue.vue";
import CreateShow from "../components/CreateShow.vue";
import UpdateShow from "../components/UpdateShow.vue";
import UserHome from "../components/UserHome.vue";
import BookingShow from "../components/BookingShow.vue";
import UserBookings from "../components/UserBookings.vue";
import ForgetPassword from "../components/ForgetPassword.vue";
import Unauthorized from "../components/Unauthorized.vue";
import ErrorPage404 from "../components/ErrorPage404.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Landing",
      component: Landing,
    },
    {
      path: "/user_login",
      name: "UserLogin",
      component: UserLogin,
    },
    {
      path: "/user_register",
      name: "UserRegister",
      component: UserRegister,
    },
    {
      path: "/admin_login",
      name: "AdminLogin",
      component: AdminLogin,
    },
    {
      path: "/admin_home",
      name: "AdminHome",
      component: AdminHome,
      meta: { adminOnly: true },
    },
    {
      path: "/create_venue",
      name: "CreateVenue",
      component: CreateVenue,
      meta: { adminOnly: true },
    },
    {
      path: "/update_venue/:id",
      name: "UpdateVenue",
      component: UpdateVenue,
      meta: { adminOnly: true },
    },
    {
      path: "/create_show/:id",
      name: "CreateShow",
      component: CreateShow,
      meta: { adminOnly: true },
    },
    {
      path: "/update_show/:id",
      name: "UpdateShow",
      component: UpdateShow,
      meta: { adminOnly: true },
    },
    {
      path: "/admin_summery",
      name: "AdminSummery",
      component: AdminSummery,
      meta: { adminOnly: true },
    },
    {
      path: "/user_home",
      name: "UserHome",
      component: UserHome,
      meta: { requiresAuth: true },
    },
    {
      path: "/booking_Show/:id",
      name: "BookingShow",
      component: BookingShow,
      meta: { requiresAuth: true },
    },
    {
      path: "/user_bookings",
      name: "UserBookings",
      component: UserBookings,
      meta: { requiresAuth: true },
    },
    {
      path: "/forget_password",
      name: "ForgetPassword",
      component: ForgetPassword,
    },
    {
      path: "/unauthorized",
      name: "Unauthorized",
      component: Unauthorized,
    },
    {
      path: "/:catchAll(.*)",
      name: "NotFound",
      component: ErrorPage404,
    }
  ]
})



router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const isAdmin = localStorage.getItem('isAdmin'); // Assuming isAdmin is stored in local storage

  if ((to.meta.requiresAuth && !token) ) {
    // Redirect to the unauthorized page if the token is missing
    next('/unauthorized');
  }
  else if(to.meta.adminOnly && !isAdmin){
    // Redirect to the admin home page if the user is an admin
    next('/unauthorized');
  }
  else{
    // Continue to the next page
    next();
  }
});



export default router;
