<template>
    <div>
        <b-row v-if="loading" class="py-4">
            <b-col>
                <h5 class="text-center">Your transaction is being processed. Please wait..</h5>
            </b-col>
        </b-row>
        <b-row no-gutters v-else class="text-center checkout-container" :class="{'no-border': payment_verification.order && payment_verification.order.is_payment_complete }">
            <template v-if="!payment_verification.enabled">
                <b-col xs="12" md="12" xl="12" id="bnomics-order-wrapper" v-if="!config.expired">
                    <b-alert variant="danger" show>
                        <b-row no-gutters align-v="center">
                            <b-col cols="2">
                                <font-awesome-icon :icon="hexagonDangerIcon" size="2x" />
                            </b-col>
                            <b-col cols="10">
                                Do not close this tab. You will be able to download the files when the payment is confirmed.
                            </b-col>
                        </b-row>
                    </b-alert>
                    <p class="pt-3 pb-1 font-weight-bold">Send exactly this amount:</p>

                    <CustomReadInput
                        id="amount-text"
                        :copy="true"
                        :external="false"
                        placeholder="Amount"
                        :value="order.expected_value"
                        :display_value="order.expected_value +' ' + order.crypto + ' ≈ ' + order.usd_price + ' USD'"
                        :icon_only="true"
                        variant="light"
                        :text_center="true"
                    />

                    <div class="divider mx-auto"></div>
            
                    <p class="py-1 font-weight-bold" >to this {{ order.crypto }} address</p>

                    <CustomReadInput
                        id="address"
                        :copy="true"
                        :external="false"
                        placeholder="Address"
                        :value="order.address"
                        :icon_only="true"
                        variant="light"
                        :text_center="true"
                    />
                
                    <div class="mt-3">
                        <a :href="payment_deeplink">
                            <b-img fluid :src="qr_url" />
                        </a>
                    </div>

                    <div class="divider mx-auto"></div>

                    <div>
                        <b-progress class="w-100" :value="timer.progress" max="600" variant="primary" height="8px"></b-progress>
                        <p class="timer mt-2 font-weight-bold" id="time" :class="{'text-danger': timer.diff<=0 }">
                            {{this.timer.minutes}} min {{this.timer.seconds}} sec left
                        </p>
                    </div> 
                </b-col>
                <b-col id="bnomics-order-expired-wrapper" v-else>
                    <h3 class="text-danger">Order Expired</h3><br>
                    <p>
                        Your order has expired.
                        <a href="#" @click.prevent="reloadPage">
                            Click here to try again
                        </a>
                    </p>
                </b-col>
            </template>
            <template v-else>
                <b-col xs="12" md="12" xl="12" class="text-center mx-auto" v-if="payment_verification.loading || !payment_verification.order || payment_verification.order.status_of_transaction == -1">
                    <div class="mb-3">
                        <font-awesome-icon :icon="spinnerIcon" spin size="3x" />
                    </div> 
                    <h3>We're verifying your payment.. Please wait..</h3>
                    <b-alert variant="warning" title="Note" show>
                        Payments may take a while to get Confirmed. You can bookmark/copy this Page URL to come back at later stage to see your Payment Status.
                        <b-form-group
                            class="mt-3"
                            label-for="product-url"
                        >
                            <b-input-group>
                                <template #append>
                                    <b-button variant="warning" @click="copy('url')">
                                        Copy to Clipboard
                                        <img id="copy-content" :src="require('@/assets/images/copy.png')" width=20px height=20px alt="Copy to clipboard">
                                    </b-button>
                                </template>
                                <b-form-input
                                    id="url"
                                    :value="public_url"
                                    placeholder="Public URL"
                                    readonly
                                    class="btn-disabled-translucent"
                                ></b-form-input>
                            </b-input-group>
                        </b-form-group>
                    </b-alert>
                    <p v-if="payment_verification.loading">
                        Getting Payment Status from Server.. Do not close or refresh this window.
                    </p>
                    <template v-else-if="payment_verification.order">
                        <p>
                            Your order status is {{ status_options[payment_verification.order.status_of_transaction] }}. If you've made the payment, stay relaxed we're still trying to confirm your order. If payment failed at your end, 
                            you can <router-link :to="{name: 'product', params: {product_uid: order.product_uid}}">Click here to try again</router-link> or 
                            <a href="#" @click.prevent="reloadPage">refresh the page</a>.
                        </p>
                    </template>
                </b-col>
                <b-col xs="12" md="12" xl="12" class="text-center mx-auto" v-else>
                    <template v-if="payment_verification.order.is_payment_complete">
                        <div class="mb-3">
                            <img :src="require('@/assets/images/tick.gif')" />
                        </div> 
                        <h3 class="text-success">Your Order is confirmed!</h3>
                        <p>We've received your payment. You'll be redirected automatically.</p>
                        <router-link :to="{name: 'order', params: {order_uid: order.uid}}">
                            Click here if you're not redirected automatically.
                        </router-link>
                    </template>
                    <template v-else>
                        <div class="mb-3 text-danger">
                            <font-awesome-icon :icon="failedIcon" size="3x" />
                        </div> 
                        
                        <h3 class="text-danger">Your Order is Failed!</h3>
                        <p>We've received your payment but it does not match the amount of the Order.</p>
                    </template>
                </b-col>
            </template>
        </b-row>
    </div>
</template>

<script>
import { faCheckCircle, faExclamationTriangle, faSpinner, faTimesCircle } from '@fortawesome/free-solid-svg-icons'
import send_request from '../utils/requests'

import CustomReadInput from "@/components/CustomReadInput"

export default {
    components: {
        CustomReadInput,
    },
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
    computed: {
        qr_url() {
            if(!this.order) return ""
            return `https://www.bitcoinqrcodemaker.com/api/?style=${this.qr_mappings[this.order.crypto]}&address=${this.order.address}&amount=${this.order.expected_value}&color=1`
        },
        payment_deeplink() {
            if(!this.order) return ""
        
            return `${this.deeplink_mappings[this.order.crypto]}:${this.order.address}?amount=${this.order.expected_value}`
        },
        spinnerIcon: () => faSpinner,
        checkCircleIcon: () => faCheckCircle,
        failedIcon: () => faTimesCircle,
        hexagonDangerIcon: () => faExclamationTriangle,
        public_url() {
            if(!this.order_uid) return null

            return window.location.protocol + "//" + window.location.host + "/checkout/" + this.order_uid
        }
    },
    mounted() {
        this.$store.dispatch('updateSidebarState', false)

        this.order_uid = this.$route.params.order_uid

        if(this.order_uid)
            this.load_data()

        this.$store.dispatch("updateSiteTitle", "Checkout")
    },
    watch: {
        // 'selected_crypto.crypto' (newV, oldV) {
        //   if(newV == oldV) return
        //   this.load_crypto_converstion_rates()
        // }
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
            this.$store.dispatch('updateHeaderTitle', this.order.product.product_name)
            this.$store.dispatch('updateHeaderSide', `Order #${this.order.uid}`)

            if(this.order.status_of_transaction > -1) {
                this.payment_verification.enabled = true
                this.payment_verification.loading = false
                this.payment_verification.order = this.order
                if(this.order.status_of_transaction == -1) {
                    // Allow Uncofirmed Downloads as long as transaction is received by PG
                    this.verify_payment_status()
                } else {
                    this.order_complete()
                }

            } else {
                this.startTimer()
                this.initializeSocket()
            }
            this.loading = false
        },
        order_complete() {
            if(this.payment_verification.order.is_payment_complete)
                setTimeout(() => this.$router.push({name: 'order', params: {order_uid: this.order.uid}}), 2000)
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
                if (parseInt(response.status) >= 0 && $this.config.accept_payments) {
                    if($this.timer_interval) clearInterval($this.timer_interval)
                    if(!$this.payment_verification.enabled) {
                        $this.payment_verification.enabled = true
                        $this.verify_payment_status()
                    }
                }
            }
        },
        verify_payment_status() {
            if(!this.payment_verification.enabled) return
            
            this.payment_verification.loading = true
            send_request({
                method: 'GET',
                url: this.$store.state.apiendpoints.order_get.replace(":order_uid", this.order_uid)
            }).then(
                (res) => {
                    this.payment_verification.order = res
                    switch(res.status_of_transaction) {
                        case -1:
                            // Awaiting Confirmation from Server
                            // Payment status is unconfirmed
                            // Payment is Partially Confirmed
                            setTimeout(this.verify_payment_status, 4000)
                        break
                        case 0:
                        case 1:
                        case 2:
                            //  Payment is Confirmed
                            this.payment_verification.loading = false
                            this.order_complete()
                    }
                    this.payment_verification.loading = false
                },
                () => {
                    this.$bvToast.toast('An Unknown Error Occurred while getting transaction status.', {
                        ...this.$store.state.common_toast_options,
                        title: 'Error',
                        variant: 'danger'
                    })
                }
            )   
        },
        specificCopy(value) {
            this.$copy_arbitary_text(value, this)
        },
        copy(id) {
            this.$copy_text(id, this)
        },
        reloadPage: () => window.location.reload()
    },
    beforeDestroy() {
        this.payment_verification.enabled = false
    }
}
</script>

<style lang="scss">

    @import "@/scss/colors";

    .btn-disabled-translucent {
        background-color: rgba(0,0,0,0.1);
    }
    .checkout-container {
        border: 1px solid #000;
        padding: 30px 40px; 
        border-radius: 10px;

        &.no-border {
            border: 0;
        }
    }

    .divider {
        width: 40px;
        height: 2px;
        background-color: #000;
        margin-top: 40px;
        margin-bottom: 40px;
    }
</style>