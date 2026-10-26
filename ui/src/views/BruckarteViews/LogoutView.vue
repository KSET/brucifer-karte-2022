<script>
import { logout } from "@/plugins/api";

export default {
    name: "Logout",
    async mounted() {
        await logout();

        this.$router.push({ name: "login" });
    },
};
</script>
