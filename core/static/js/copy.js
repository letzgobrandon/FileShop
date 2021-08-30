var app = new Vue({
    ...common_vue_config,
    data: {

      product_uid: null,
      product_token: null,
      user_data: {
        email: null,
      },
  
      submit_disabled: true,
      api_errors: {},

      dashboard_url: null
    },
    computed: {
      public_url() {
        if(!this.product_uid) return null

        return window.location.protocol + "//" + window.location.host + "/" + static_urls.product_public_url.replace(":uid", this.product_uid)
      }
    },
    mounted() {
      hide_preloader()
      this.get_data()
    },
    methods: {
      get_data() {

        let query_params = new URLSearchParams(window.location.search)
        
        this.product_uid = query_params.get('uid')
        this.product_token = query_params.get('token')
        this.submit_disabled = false
      },
      save() {

        send_request({
          method: 'PATCH',
          url: `${apiendpoints.product_get}/${this.product_uid}`,
          data: {"token":  this.product_token, "email": this.user_data.email}
        }).then(
          (res) => {
            this.dashboard_url = window.location.protocol + "//" + window.location.host + "/" + static_urls.seller_dashboard.replace(":token", this.product_token)
            window.location.href = this.dashboard_url
          },
          (err) => {
            
            let response = err.response
            if(response.status == 400) {
              this.api_errors = response.data.error
            } else {
              this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
                ...this.toast_options,
                title: 'Error',
                variant: 'danger'
              })
            }
          
            this.submit_disabled = false
          }
        )
      },
      copy(id) {
        copy_text(id, this)
      }
    }
  })
  Vue.use(window.BootstrapVue)
  