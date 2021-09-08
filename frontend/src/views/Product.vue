<template>
    <div>
        <b-row no-gutters>
            <b-col cols="12" md="12">
                <img class="card-img-top" :src="require('@/assets/images/product_placeholder.png')" alt="Card Image Cap">
            </b-col>
            <b-col cols="12" md="12" class="px-4 py-2">
                <h5 class="card-title">
                    <template v-if="loading">
                        Loading...
                    </template>
                    <template v-else>
                        {{ product.product_name || "No Name" }}
                    </template>
                </h5>
                <p class="card-text">
                    <template v-if="loading">
                        Loading...
                    </template>
                    <template v-else>
                        {{ product.product_description || "No Description" }}
                    </template>
                </p>
                <p>
                    <strong>Total files: </strong> 
                    <template v-if="loading">
                        Loading...
                    </template>
                    <template v-else>
                        {{ product.num_files || 0 }}
                    </template>
                </p>
                <p class="text-left">
                    <strong>Price: </strong>
                    <template v-if="loading">
                        Loading...
                    </template>
                    <template v-else>
                        <strong>{{ product.price }}</strong> {{ product.currency }}
                    </template>
                </p>
            </b-col>
            <b-col cols="12" md="12" class="px-4 py-2 text-left d-flex">
                <strong class="mr-2">Buy Using: </strong>
                <template v-if="loading">
                    Loading...
                </template>
                <template v-else>
                    <b-form-select
                        :options="crypto_options"
                        v-model="selected_crypto.crypto"
                        style="max-width: 150px;"
                    ></b-form-select>

                    <div class="ml-auto">
                        <template v-if="!buying_info.loading">
                            <b-button variant="info" pill :disabled="submit_disabled || !selected_crypto.crypto || selected_crypto.loading" class="d-block w-100" @click.prevent="initiate_transaction">
                                Buy Now
                            </b-button>
                        </template>
                        <template v-else>
                            <b-button variant="info" pill :disabled="true" class="d-block w-100">
                                ...
                            </b-button>
                        </template>
                    </div>
                </template>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import send_request from '../utils/requests'
export default {
    data() {
        return {
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
        }
    },
    mounted() {
      this.product_uid = this.$route.params.product_uid
      this.$store.dispatch('updateSidebarState', false)

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
        load_data() {
            this.loading = true
            send_request({
                method: 'GET',
                url: this.$store.state.apiendpoints.product_get + "/" + this.product_uid
            }).then(
                (res) => {
                    this.product = res
                    this.loading = false
                    this.$store.dispatch("updateSiteTitle", res.product_name || "Buy Product")
                    // if(this.selected_crypto.crypto)
                    //   this.load_crypto_converstion_rates()
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
                url: this.$store.state.apiendpoints.order_create,
                data: payload
            }).then(
                (res) => {
                    this.$router.push({name: 'checkout', params: {order_uid: res.order_uuid}})
                    // let order_uid = res.order_uuid
                    // window.location.href = `/${static_urls.checkout.replace(':order_uuid', order_uid)}`
                },
                () => {
                    this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
                        ...this.$store.state.common_toast_options,
                        title: 'Error',
                        variant: 'danger'
                    })
                    this.buying_info.loading = false
                }
            )
        }
    }
}
</script>