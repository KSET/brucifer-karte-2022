<template>
    <div>
        <Sidebar />
        <div class="admin-page-container">
            <LineupAdd></LineupAdd>
        </div>
    </div>
</template>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

import LineupAdd from '@/components/Lineup/LineupAdd.vue';
export default {
    components: { LineupAdd,Sidebar }
}
</script>

<style>

</style>