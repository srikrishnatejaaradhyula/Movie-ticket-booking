<template>
    <div>
        <div class="login">
            <h1>Login</h1>
            <form>
                <input type="text" placeholder="Username" />
                <input type="password" placeholder="Password" />
                <button type="submit">Login</button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Login'
}
</script>

<style scoped>
.login {
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: center;
    height: 100vh;
    margin: 0 auto;
    width: 30%;
}
input{
    margin: 10px 0;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: 300px;
}
button{
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: 300px;
    background-color: #ccc;
    cursor: pointer;
}


</style>