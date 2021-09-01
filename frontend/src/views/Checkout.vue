<template>
    <div>
        <b-row v-if="loading" class="py-4">
            <b-col>
                <h5 class="text-center">Your transaction is being processed. Please wait..</h5>
            </b-col>
        </b-row>
        <b-row no-gutters v-else class="text-center">
            <template v-if="!payment_verification.enabled">
                <b-col xs="12" md="4" xl="4">
                    <span>
                        <a :href="payment_deeplink">
                            <b-img fluid :src="qr_url" />
                        </a>
                    </span>
                </b-col>
                <b-col xs="12" md="8" xl="6">
                    <div id="bnomics-order-wrapper" v-if="!config.expired">
                
                        <p class="payment_message pt-3 pb-1">To pay, send exactly this {{ this.order.crypto }} amount</p>
                
                        <div class="cursor-pointer payment-border rounded text-dark mx-0 my-1 p-2" @click="specificCopy(order.expected_value)">
                            <img class="float-right" :src="require('@/assets/images/copy.png')" width=30px height=30px alt="Copy to clipboard">
                            <p class="h6 text-center" id="amount_text">{{ order.expected_value }} {{ order.crypto }} ≈ {{ order.usd_price }} USD</p>
                        </div>
                
                        <p class="payment_message py-1" >to this {{ order.crypto }} address</p>
                
                        <div class="cursor-pointer payment-border rounded text-dark mx-0 my-1 p-2" @click.prevent="specificCopy(order.address)">
                            <img class="float-right" :src="require('@/assets/images/copy.png')" width=30px height=30px alt="Copy to clipboard">
                            <p class="h6 text-center" id="address_text">{{ order.address }}</p>
                        </div>
                        
                        <progress class='w-75' :value="timer.progress" max="600" id="progressBar"></progress>
                        <p class="timer" id="time" :class="{'text-danger': timer.diff<=0 }">
                            {{this.timer.minutes}} : {{this.timer.seconds}} min
                        </p>
                    </div>
                
                    <div id="bnomics-order-expired-wrapper" v-else>
                        <h3 class="warning bnomics-status-warning">Order Expired</h3><br>
                        <p class="click-to-try-again cursor-pointer"><a onClick="window.location.reload()">Click here to try again</a></p>
                    </div>
                </b-col>
            </template>
            <template v-else>
                <b-col xs="12" md="12" xl="12" class="text-center mx-auto" v-if="payment_verification.loading || !payment_verification.order || payment_verification.order.status_of_transaction < 2">
                    <h3>We're verifying your payment.. Please wait..</h3>
                    <p v-if="payment_verification.loading">
                        Getting Payment Status from Server.. Do not close or refresh this window.
                    </p>
                    <p v-else-if="payment_verification.order">
                        Your order status is {{ status_options[payment_verification.order.status_of_transaction] }}. If you've made the payment, stay relaxed we're still trying to confirm your order. If payment failed at your end, you can <a onClick="window.location.reload()">Click here to try again</a>.
                    </p>
                </b-col>
                <b-col xs="12" md="12" xl="12" class="text-center mx-auto" v-else>
                    <h3 class="text-success">Your Order is confirmed!</h3>
                </b-col>
            </template>
        </b-row>
    </div>
</template>

<script>
import send_request from '../utils/requests'
export default {
    data() {
        return {
            order_uid: null,
            order: null,
          
            config: {
                accept_payments: true,
                expired: false,
            },
            status_options: {
                "-1": "Pending Verification",
                "0": "Unconfirmed", 
                "1": "Partially Confirmed", 
                "2": "Confirmed"
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
            },
            payment_verification: {
                enabled: false,
                loading: false,
                order: null
            }
        }
    },
    mounted() {
        this.$store.dispatch('updateSidebarState', false)

        this.order_uid = this.$route.params.order_uid

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
        
        load_data() {
            this.loading = true
            send_request({
                method: 'GET',
                url: this.$store.state.apiendpoints.order_get.replace(":order_uid", this.order_uid)
            }).then(
                (res) => {
                    this.order = res
                    this.init()
                },
                () => {
                    this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
                        ...this.$store.state.common_toast_options,
                        title: 'Error',
                        variant: 'danger'
                    })
                }
            )
        },
        init() {
            if(this.order.status_of_transaction == 2) {
                this.payment_verification.enabled = true
                this.payment_verification.loading = false
                this.payment_verification.order = this.order

            } else {
                this.startTimer()
                this.initializeSocket()
            }
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

                if($this.timer.diff<=0) {
                    $this.config.accept_payments = false;
                    clearInterval($this.timer_interval);
                    $this.config.expired = true
                }
            }
            this.timer_interval = setInterval(calculate_time, 1000);
            calculate_time()
        },
        initializeSocket() {
            this.socket_config.connection = new WebSocket(
                "wss://www.blockonomics.co/payment/"+ this.order.address
            )
            let $this = this
            this.socket_config.connection.onmessage = function(event) {
                let response = JSON.parse(event.data)
                console.log(response)
                if (parseInt(response.status) >= 0 && $this.config.accept_payments) {
                    // console.log("Sending Request")
                    // setTimeout(
                    //     $this.paymentStatusUpdate(response.status),
                    //     1000
                    // )
                    if($this.timer_interval) clearInterval($this.timer_interval)
                    if(!$this.payment_verification.enabled) {
                        $this.payment_verification.enabled = true
                        $this.verify_payment_status()
                    }
                }
            }
        },
        verify_payment_status() {
            this.payment_verification.loading = true
            send_request({
                method: 'GET',
                url: this.$store.state.apiendpoints.order_get.replace(":order_uid", this.order_uid)
            }).then(
                (res) => {
                    this.payment_verification.order = res
                    switch(res.status_of_transaction) {
                        case -1:
                        case 0:
                        case 1:
                            // Awaiting Confirmation from Server
                            // Payment status is unconfirmed
                            // Payment is Partially Confirmed
                            setTimeout(this.verify_payment_status, 4000)
                        break
                        case 2:
                            //  Payment is Confirmed
                            this.payment_verification.loading = false
                            // do other stuff
                    }
                    this.payment_verification.loading = false
                },
                () => {
                    this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
                        ...this.$store.state.common_toast_options,
                        title: 'Error',
                        variant: 'danger'
                    })
                }
            )   
        },
        specificCopy(value) {
            this.$copy_arbitary_text(value, this)
        }
    },
    beforeDestroy() {
        this.payment_verification.enabled = false
    }
}
</script>