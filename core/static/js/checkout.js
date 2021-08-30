var app = new Vue({
  ...common_vue_config,
  data: {
    order_uid: null,
    order: null,
  
    config: {
      accept_payments: true,
      expired: false,
    },

    crypto_options: [
      { value: 'BTC', text: 'Bitcoin (BTC)' },
    ],
    qr_mappings: {
      "BTC": "bitcoin",
      "BCH": "bitcoincash"
    },
    deeplink_mappings: {
      "BTC": "bitcoin",
      "BCH": "bitcoincash"
    },

    submit_disabled: false,
    api_errors: {},
    loading: true,

    timer: {
      start: null,

      diff: 0,
      duration: 60 * 10, // Ten Minutes
      minutes: 0,
      seconds: 0,
      progress: 0
    },

    socket_config: {
      connection: null
    }

  },
  mounted() {
    hide_preloader()

    this.order_uid = this.get_order_uid_from_url()

    if(this.order_uid)
      this.load_data()
    
  },
  watch: {
    // 'selected_crypto.crypto' (newV, oldV) {
    //   if(newV == oldV) return
    //   this.load_crypto_converstion_rates()
    // }
  },
  computed: {
    qr_url() {
      if(!this.order) return ""
      return `https://www.bitcoinqrcodemaker.com/api/?style=${this.qr_mappings[this.order.crypto]}&address=${this.order.address}&amount=${this.order.expected_value}&color=1`
    },
    payment_deeplink() {
      if(!this.order) return ""
      
      return `${this.deeplink_mappings[this.order.crypto]}:${this.order.address}?amount=${this.order.expected_value}`
    }
  },
  methods: {
    get_order_uid_from_url() {
      let url_pattern = new RegExp("\/checkout\/([0-9a-f-]+)\/?", "g")
      let match = url_pattern.exec(window.location.pathname)
      
      if(match.length)
        return match[1]
    },
    load_data() {
      this.loading = true
      send_request({
        method: 'GET',
        url: apiendpoints.order_get.replace(":order_uid", this.order_uid)
      }).then(
        (res) => {
          this.order = res
          this.init()
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
    init() {
      this.startTimer()
      this.initializeSocket()

      this.loading = false
    },
    startTimer() {
      if(this.timer_interval) clearInterval(this.timer_interval)

      this.timer.start = Date.now();
      this.timer.duration = 60*10;

      // This needs to be discussed. Instead of session it should consider time from creating of address.
      // if(last_order){
      //     //reduce the 10 minutes duration by the time at which the given order was put in session
      //     duration-=((start-(new Date(parseInt(last_order)*1000)))/1000 | 0);
      // }

      let $this = this
      
      function calculate_time() {
        $this.timer.diff = $this.timer.duration - (((Date.now() - $this.timer.start) / 1000) | 0);
        $this.timer.minutes = ($this.timer.diff / 60) | 0;
        $this.timer.seconds = ($this.timer.diff % 60) | 0;

        $this.timer.minutes = $this.timer.minutes < 10 ? "0" + $this.timer.minutes : $this.timer.minutes;
        $this.timer.seconds = $this.timer.seconds < 10 ? "0" + $this.timer.seconds : $this.timer.seconds;

        $this.timer.progress = 600 - (600 - $this.timer.diff);

        // display.textContent = $this.timer.minutes + ":" + $this.timer.seconds + " min"; 

        if($this.timer.diff<=0) {
          
          $this.config.accept_payments = false;

          clearInterval($this.timer_interval);

          $this.config.expired = true

          // document.getElementById("bnomics-order-expired-wrapper").style.display = "block";
          // document.getElementById("bnomics-order-wrapper").style.display = "none";
        }
      }
      this.timer_interval = setInterval(calculate_time, 1000);
      calculate_time()
    },
    initializeSocket() {
      this.socket_config.connection = new WebSocket(
        "wss://www.blockonomics.co/payment/"+ this.order.address
      )
      this.socket_config.connection.onmessage = function(event) {
        let response = JSON.parse(event.data)
        if (parseInt(response.status) >= 0 && this.config.accept_payments) {
          console.log("Sending Request")
          setTimeout(
            this.paymentStatusUpdate(response.status),
            1000
          )
        }
      }
    },
    paymentStatusUpdate(status) {
      send_request({
        method: 'POST',
        url: apiendpoints.order_callback.replace(":order_uid", this.order_uid)
      }).then(
        (res) => {
          console.log("Success")
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
    specificCopy(value) {
      copy_arbitary_text(value, this)
    }
  }
})
Vue.use(window.BootstrapVue)
  