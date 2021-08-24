var app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'], // Override Conflicting Delimiters because of DTL
    data: {
      toast_options: {
        autoHideDelay: 5000,
        appendToast: false,
        variant: 'success',
        toaster: 'b-toaster-bottom-center'
      },

      product_uid: null,
      product: null,

      selected_crypto: {
        crypto: 'BTC',
        details: {},
        loading: true
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
      document.getElementById("preloader").style.top = "-120vh"
      setTimeout(() => {
        document.getElementById("preloader").style.display = "none"
      }, 2000)

      this.product_uid = this.get_product_uid_from_url()

      if(this.product_uid)
        this.load_data()
      
    },
    watch: {
      'selected_crypto.crypto' (newV, oldV) {
        if(newV == oldV) return
        this.load_crypto_converstion_rates()
      }
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
        axios({
          method: 'GET',
          url: apiendpoints.product_get + this.product_uid,
          withCredentials: true
        }).then(
          (res) => {
            this.product = res.data
            this.loading = false
            if(this.selected_crypto.crypto)
              this.load_crypto_converstion_rates()
          },
          (err) => {
            if(!err.response) {
              this.$bvToast.toast('A Network Error Occurred. Please check your internet connection and try Again.', {
                ...this.toast_options,
                title: 'Network Error',
                variant: 'danger'
              })
            } else {
              this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
                ...this.toast_options,
                title: 'Error',
                variant: 'danger'
              })
            }
          }
        )
      },
      load_crypto_converstion_rates() {
        if(!this.selected_crypto.crypto) return
        
        this.selected_crypto.loading = true

        let payload = {
          currency: this.product.currency,
          price: this.product.price,
          crypto: this.selected_crypto.crypto
        }
        axios({
          method: 'POST',
          url: apiendpoints.currency_converter,
          withCredentials: true,
          data: payload
        }).then(
          (res) => {
            this.selected_crypto.details = res.data
            this.selected_crypto.loading = false
          },
          (err) => {
            if(!err.response) {
              this.$bvToast.toast('A Network Error Occurred. Please check your internet connection and try Again.', {
                ...this.toast_options,
                title: 'Network Error',
                variant: 'danger'
              })
            } else {
              this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
                ...this.toast_options,
                title: 'Error',
                variant: 'danger'
              })
            }
          }
        )
      },
      initiate_transaction() {

        if(!this.selected_crypto.crypto) return
        
        this.buying_info.loading = true

        let payload = {
          crypto: this.selected_crypto.crypto
        }

        axios({
          method: 'POST',
          url: apiendpoints.product_get + this.product_uid + "/initiate-transaction",
          withCredentials: true,
          data: payload
        }).then(
          (res) => {
            window.location = res.data.payment_url
          },
          (err) => {
            if(!err.response) {
              this.$bvToast.toast('A Network Error Occurred. Please check your internet connection and try Again.', {
                ...this.toast_options,
                title: 'Network Error',
                variant: 'danger'
              })
            } else {
              this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
                ...this.toast_options,
                title: 'Error',
                variant: 'danger'
              })
            }
          }
        )
      }
    }
  })
  Vue.use(window.BootstrapVue)
  