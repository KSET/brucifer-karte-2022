<script>
import store from '@/store/index.js';
export default {
    name: 'Logout',
    components: {
    },
    el: '#app',
    mounted() {
        console.log("ye")
        store.commit('setId', '')
        store.commit('setName', '')
        store.commit('setEmail', '')
        store.commit('setPrivilege', '')
        store.commit('setTokenExp', 10000000000000000)
        console.log("User logged out")
        this.$router.push({ name: "login" })
    }
}
</script>

<style scoped>

</style>


