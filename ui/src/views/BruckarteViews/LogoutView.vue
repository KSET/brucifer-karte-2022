<script>
import store from "@/store/index.js";

export default {
    name: "Logout",
    mounted() {
        store.commit("clearAuth");

        this.$router.push({ name: "login" });
    },
};
</script>
