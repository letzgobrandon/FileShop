var app = new Vue({
    ...common_vue_config,
    data: {
      product_uid: null,
      product: null,

      selected_crypto: {
        crypto: 'BTC',
        // details: {},
        loading: false
      },

      crypto_options: [
        { value: 'BTC', text: 'Bitcoin (BTC)' },
      ],
  
      submit_disabled: false,
      api_errors: {},
      loading: true,

      buying_info: {
        loading: false
      }
    },
    mounted() {
      hide_preloader()

      this.product_uid = this.get_product_uid_from_url()

      if(this.product_uid)
        this.load_data()
      
    },
    watch: {
      // 'selected_crypto.crypto' (newV, oldV) {
      //   if(newV == oldV) return
      //   this.load_crypto_converstion_rates()
      // }
    },
    methods: {
      get_product_uid_from_url() {
        let url_pattern = new RegExp("\/product\/([0-9a-f-]+)\/", "g")
        let match = url_pattern.exec(window.location.pathname)
        
        if(match.length)
          return match[1]

      },
      load_data() {
        this.loading = true
        send_request({
          method: 'GET',
          url: apiendpoints.product_get + "/" + this.product_uid
        }).then(
          (res) => {
            this.product = res
            this.loading = false
            // if(this.selected_crypto.crypto)
            //   this.load_crypto_converstion_rates()
          },
          (err) => {
            this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
              ...common_toast_options,
              title: 'Error',
              variant: 'danger'
            })
          }
        )
      },
      // load_crypto_converstion_rates() {
      //   if(!this.selected_crypto.crypto) return
        
      //   this.selected_crypto.loading = true

      //   let payload = {
      //     currency: this.product.currency,
      //     price: this.product.price,
      //     crypto: this.selected_crypto.crypto
      //   }
      //   send_request({
      //     method: 'POST',
      //     url: apiendpoints.currency_converter,
      //     data: payload
      //   }).then(
      //     (res) => {
      //       this.selected_crypto.details = res
      //       this.selected_crypto.loading = false
      //     },
      //     (err) => {
      //       this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
      //         ...common_toast_options,
      //         title: 'Error',
      //         variant: 'danger'
      //       })
      //     }
      //   )
      // },
      initiate_transaction() {

        if(!this.selected_crypto.crypto) return
        
        this.buying_info.loading = true

        let payload = {
          crypto: this.selected_crypto.crypto,
          product_uid: this.product_uid
        }

        send_request({
          method: 'POST',
          url: apiendpoints.order_create,
          data: payload
        }).then(
          (res) => {
            let order_uid = res.order_uuid
            window.location.href = `/${static_urls.checkout.replace(':order_uuid', order_uid)}`
          },
          (err) => {
            this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
              ...common_toast_options,
              title: 'Error',
              variant: 'danger'
            })
          }
        )
      }
    }
  })
  Vue.use(window.BootstrapVue)
  