<script>
import store from '@/store/index.js';
export default {
    name: 'Logout',
    components: {
    },
    el: '#app',
    mounted() {
        store.commit('setId', '')
        store.commit('setName', '')
        store.commit('setEmail', '')
        store.commit('setPrivilege', '')
        console.log("User logged out")
        this.$router.push({ name: "login" })
    }
}
</script>


