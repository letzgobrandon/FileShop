<template>
    <div>
        <b-row no-gutters>
            <b-col cols="12" md="12" class="px-4 py-2">
                <h3 class="card-title text-underline">
                    Description
                </h3>
                <p class="card-text">
                    <template v-if="loading">
                        Loading...
                    </template>
                    <template v-else>
                        {{ product.product_description || "No Description" }}
                    </template>
                </p>
            </b-col>
            <b-col cols="12" md="12" class="px-4 py-2">
                <h5 class="card-title text-underline">
                    Overview
                </h5>
                <div class="overview-table" v-if="!loading">
                    <b-table-simple
                        class="mt-3 text-center" 
                        responsive
                    >
                        <template #table-busy>
                            <div class="text-center text-primary my-2">
                                <b-spinner class="align-middle"></b-spinner>
                                <strong class="d-block">Loading</strong>
                            </div>
                        </template>

                        <b-tbody>
                            <b-tr v-for="(data, index) in product.files" :key="index">
                                <!-- Icon -->
                                <b-td>
                                    <FileIcon :name="data.file_name" />
                                </b-td>

                                <!-- File Name -->
                                <b-td class="text-left text-capitalize">
                                    {{ data.file_name }}
                                </b-td>

                                <!-- Size -->
                                <b-td>
                                    <BytesToHuman :bytes="data.file_size" />
                                </b-td>
                            </b-tr>
                        </b-tbody>
                    </b-table-simple>
                </div>
            </b-col>
            
            <b-col cols="12" md="12" class="px-4 py-2">
                <b-row no-gutters>
                    <b-col cols="12" md="4" class="text-center">
                        <h5 class="card-title text-underline">
                            Total Files
                        </h5>
                        <h5>
                            <template v-if="loading">
                                Loading...
                            </template>
                            <template v-else>
                                {{ product.num_files || 0 }}
                            </template>
                        </h5>
                    </b-col>
                    <b-col cols="12" md="4" class="text-center">
                        <h5 class="card-title text-underline">
                            Total Size
                        </h5>
                        <h5>
                            <BytesToHuman :bytes="product.files.reduce((p, c) => p + c.file_size, 0)" />
                        </h5>
                    </b-col>
                    <b-col cols="12" md="4" class="text-center">
                        <h5 class="card-title text-underline">
                            Total Price
                        </h5>
                        <h5>
                            <template v-if="loading">
                                Loading...
                            </template>
                            <template v-else>
                                <strong>{{ product.price }}</strong> {{ product.currency }}
                            </template>
                        </h5>
                    </b-col>
                </b-row>
            </b-col>
            <b-col cols="12" md="12" class="px-4 py-2">
                <b-row no-gutters>
                    <b-col cols="12" :md="$store.state.options.disable_bch ? 12 : 6" class="text-center mt-2">
                        <BitcoinButton 
                            :disable_amount="true"
                            label="Pay with BTC"
                            variant="btc"
                            class="mx-2"
                            @input="initiate_transaction('BTC')"
                            :disabled="buying_info.loading"
                        />
                    </b-col>
                    <b-col cols="12" md="6" class="text-center mt-2" v-if="!$store.state.options.disable_bch">
                        <BitcoinButton 
                            :disable_amount="true"
                            label="Pay with BCH"
                            variant="bch"
                            class="mx-2"
                            @input="initiate_transaction('BCH')"
                            :disabled="true"
                        />
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import send_request from '../utils/requests'

import BytesToHuman from "@/components/BytesToHuman"
import FileIcon from "@/components/FileIcon"
import BitcoinButton from "@/components/BitcoinButton"

export default {
    components: {
        BytesToHuman,
        FileIcon,
        BitcoinButton
    },
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
            },
            // converted_rates: {
            //     bch: { 
            //         loading: false,
            //         value: 0
            //     },
            //     btc: { 
            //         loading: true,
            //         value: 0
            //     },
            // },
            overview_fields: [
                { key: 'file_icon', label: '', class: 'text-center'},
                { key: 'file_name', label: 'File Name'},
                { key: 'file_size', label: 'File Size', class: 'text-center'},
            ]
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
                    this.$store.dispatch('updateHeaderTitle', this.product.product_name)
                    this.$store.dispatch('updateHeaderSide', null)
                    
                    // this.load_crypto_converstion_rates()
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
        //     ['btc', 'bch'].forEach(crypto => {
        //         if(crypto == 'bch') return
        //         this.converted_rates[crypto].loading = true
      
        //         let payload = {
        //             currency: this.product.currency,
        //             price: this.product.price,
        //             crypto: crypto.toUpperCase()
        //         }

        //         send_request({
        //             method: 'POST',
        //             url: this.$store.state.apiendpoints.currency_converter,
        //             data: payload
        //         }).then(
        //             (res) => {
        //                 this.converted_rates[crypto].value = res
        //                 this.converted_rates[crypto].loading = false
        //             },
        //             (err) => {
        //                 if(err.response && err.response.status == 400 && err.response.data.error && err.response.data.error.currency) {
        //                     this.$bvToast.toast(err.response.data.error.currency, {
        //                         ...this.$store.state.common_toast_options,
        //                         title: 'Error',
        //                         variant: 'danger'
        //                     })
        //                 } else {
        //                     this.$bvToast.toast(`An Unknown Error Occurred while loading conversion rates for ${crypto} !`, {
        //                         ...this.$store.state.common_toast_options,
        //                         title: 'Error',
        //                         variant: 'danger'
        //                     })
        //                 }
        //             }
        //         )
        //     })
        // },
        initiate_transaction(crypto) {

            if(!crypto) return
            
            this.buying_info.loading = true

            let payload = {
                crypto: crypto,
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

<style lang="scss">

@import '@/scss/colors.scss';

.overview-table {
    border: 1px solid $primary-color;
    border-radius: 20px;

    .table th, .table td {
        border-top: none;
    }
}
</style>