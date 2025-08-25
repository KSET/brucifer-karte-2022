<template>
    <div class="footery">
        <p id="text1" class="footer-text"> © KSET {{ year }}</p>

        <div class="footer-left-container">
            <div v-if="IGRICA_VISIBILITY != 0">
                <router-link class="footer-text" to="/uvjeti-koristenja">
                    <p class="footer-text">Uvjeti korištenja</p>
                </router-link>
            </div>
            <router-link class="footer-text" style="margin-left:30px" to="/pravila-ponasanja">
                <p class="footer-text">Pravila ponašanja</p>
            </router-link>
        </div>
    </div>
</template>


<script>
import visibilityStore from '@/store/visibilityStore';

export default {
    name: "Footer",
    data() {
        return {
            year: new Date().getFullYear(),
        }
    },
    computed: {
        IGRICA_VISIBILITY() {
            return visibilityStore.state.IGRICA_VISIBILITY;
        }
    }
}

</script>

<style>
.footery {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 60px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  background: var(--bw-footer-color);
  padding: 0 3%;
}

.footer-left-container {
  display: flex;
  align-items: center;
  gap: 30px; 
}

.footer-text {
  margin: 0; 
  font: 400 14px/14px Ubuntu, sans-serif;
  letter-spacing: -0.022em;
  text-align: right;
  color: #fff;
  text-decoration: none; 
}

.footer-text:hover {
  color: #dbe9f4;
}
</style>
