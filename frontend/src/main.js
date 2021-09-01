import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'

Vue.config.productionTip = false

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

Vue.prototype.$copy_text = (id, vue_instance=null) => {
  const copyText = document.getElementById(id);

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  /* Copy the text inside the text field */
  document.execCommand("copy");

  if(vue_instance) {
    vue_instance.$bvToast.toast('URL Copied Succesfully!', {
      title: 'Success',
      ...store.state.common_toast_options,
    })
  }
}

Vue.prototype.$copy_arbitary_text = (value, vue_instance=null) => {
  // Insert a temporary field in DOM
  const copyText = document.createElement("input")
  let id = "temp-" + Date.now()
  copyText.id = id
  copyText.value = value
  copyText.style.opacity = 0
  document.getElementsByTagName("body")[0].append(copyText)

  /* Select the text field */
  let inserted_field = document.getElementById(id)
  inserted_field.select();
  inserted_field.setSelectionRange(0, 99999); /* For mobile devices */

  /* Copy the text inside the text field */
  document.execCommand("copy");
  
  // Remove the temporary field from DOM
  inserted_field.remove()

  if(vue_instance) {
    vue_instance.$bvToast.toast('URL Copied Succesfully!', {
      title: 'Success',
      ...store.state.common_toast_options,
    })
  }
}

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

Vue.component('font-awesome-icon', FontAwesomeIcon)


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
