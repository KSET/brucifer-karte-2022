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
        store.commit('setTokenExp', 10000000000000000)
        this.$router.push({ name: "login" })
    }
}
</script>




