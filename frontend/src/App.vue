<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import "./scss/main.scss"

export default {
  created() {
    window.addEventListener("swRegistered", (e) => {
      console.log(e)
      this.$store.dispatch('updateServiceWorker', e.detail.registration)
    });
    window.addEventListener("swUpdateAvailable", (e) => {
      e.detail.worker.postMessage({type: 'SKIP_WAITING'});
    });
  },
}
</script>