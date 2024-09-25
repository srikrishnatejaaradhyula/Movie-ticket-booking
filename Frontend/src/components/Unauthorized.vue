<template>
    <div class="container pt-5 mt-5">
        <div class="row justify-content-center align-content-center">
            <div class="col-md-6">
                <img src="src\assets\403-forbidden.jpg" alt="error" class="img-fluid">
            </div>
            <div class="col-md-6">
                <h1>Unauthorized</h1>
                <p>You are not authorized to access this page.</p>
                <router-link to="/" class="btn btn-primary">Go to LoginPage</router-link>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: "Unauthorized",
};
</script>
  