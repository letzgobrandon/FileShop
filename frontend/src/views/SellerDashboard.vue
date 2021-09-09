<template>
    <div>
        <template v-if="!loading">
            <b-row>
                <b-col cols="12" md="7" lg="7">
                    <b-tabs content-class="mt-3">
                        <b-tab title="Orders" active lazy>
                            <ListOrders 
                                :product="product"
                            />
                        </b-tab>
                        <b-tab title="Withdrawl Requests" lazy>
                            <ListWithdrawls 
                                :product="product"
                            />
                        </b-tab>
                    </b-tabs>
                </b-col>
                <b-col cols="12" md="5" lg="5">
                    <b-row no-gutters>
                        <b-col>
                            <div class="mb-3">
                                <h5 class="d-inline">
                                    "{{ product.product_name || "Public" }}" URL:
                                </h5>
                                <b-badge pill variant="primary" class="float-right">
                                    <font-awesome-icon :icon="eyeIcon" /> {{ product.hits }}
                                </b-badge>
                            </div>
                            <CustomReadInput
                                id="product-url"
                                :copy="true"
                                :external="true"
                                placeholder="Public URL"
                                :value="public_url"
                                :icon_only="true"
                            />
                            <p class="mt-2">Share this link with your clients.</p>
                        </b-col>
                    </b-row>
                    <b-row no-gutters class="mt-3">
                        <b-col>
                            <div class="mb-3">
                                <h5 class="d-inline">
                                    Balances
                                </h5>
                            </div>
                            <div class="d-flex justify-content-center">
                                <BitcoinButton 
                                    :amount="balances.data.btc"
                                    label="withdraw"
                                    variant="btc"
                                    class="mx-2"
                                    @input="do_withdraw('btc')"
                                    :hide_right="!balances.data.btc || balances.data.btc <= 0"
                                    :loading="this.balances.loading"
                                />
                                <BitcoinButton 
                                    :amount="balances.data.bch"
                                    label="withdraw"
                                    variant="bch"
                                    class="mx-2"
                                    @input="do_withdraw('btc')"
                                    :hide_right="!balances.data.bch || balances.data.bch <= 0"
                                    :loading="this.balances.loading"
                                />
                            </div>
                        </b-col>
                    </b-row>
                    <b-row no-gutters class="mt-3">
                        <b-col cols="12">
                            <div class="mb-3">
                                <h5 class="d-inline">
                                    Keep Access to your dashboard:
                                </h5>
                            </div>
                        </b-col>
                        <b-col cols="12">
                            <EmailUpdate :product="product" />
                        </b-col>
                        <b-col cols="12">
                            <p>Your email will be used to receive updates on payments and send your dashboard URL on demand.</p>
                            <b-alert :show="!product.email" variant="danger">
                                <b-row no-gutters align-v="center">
                                    <b-col cols="2">
                                        <font-awesome-icon :icon="hexagonDangerIcon" size="2x" />
                                    </b-col>
                                    <b-col cols="10">
                                        It is highly recommended that you specify an email address to receive link to this page and updates 
                                        of sales. Alternatively, copy and keep this page’s URL safely as it is the only way to withdraw your 
                                        earnings.
                                    </b-col>
                                </b-row>
                            </b-alert>
                        </b-col>
                    </b-row>
                </b-col>
            </b-row>

            <b-modal centered title="Withdraw" v-model="withdrawl_form.active" hide-footer>
                <WithdrawlForm 
                    :product="product"
                    :crypto="withdrawl_form.crypto"
                    :balances="balances.data"
                    @success="closePopup"
                />
            </b-modal>
        </template>
    </div>
</template>

<script>
import send_request from '../utils/requests'

import { faExclamationTriangle, faEye } from '@fortawesome/free-solid-svg-icons'
import CustomReadInput from "@/components/CustomReadInput"
import BitcoinButton from "@/components/BitcoinButton"
import ListOrders from "./components/ListOrders.vue"
import ListWithdrawls from "./components/ListWithdrawls.vue"
import EmailUpdate from  "./components/Email.vue"
import WithdrawlForm from  "./components/WithdrawlForm.vue"

export default {
    components: {
        ListOrders,
        CustomReadInput,
        BitcoinButton,
        EmailUpdate,
        WithdrawlForm,
        ListWithdrawls
    },
    data() {
        return {
            product: null,
            loading: true,

            balances: {
                loading: true,
                data: {
                    btc: 0,
                    bch: 0
                }
            },

            withdrawl_form: {
                active: false,
                crypto: null
            }
        }
    },
    computed: {
        eyeIcon: () => faEye,
        hexagonDangerIcon: () => faExclamationTriangle,
        public_url() {
            if(!this.product) return null

            return window.location.protocol + "//" + window.location.host + "/product/" + this.product.uid
        }
    },
    mounted() {
      this.product_token = this.$route.params.product_token
      this.product_uid = this.$route.params.product_uid
      this.$store.dispatch('updateSidebarState', false)

      if(this.product_uid && this.product_token)
        this.load_data()
    },
    methods: {
        load_data() {
            this.loading = true
            send_request({
                method: 'GET',
                url: this.$store.state.apiendpoints.product_get + "/" + this.product_uid,
                params: {
                    token: this.product_token
                }
            }).then(
                (res) => {
                    this.product = res
                    this.loading = false
                    this.$store.dispatch("updateSiteTitle", `${res.product_name} | Seller Dashboard` || "Seller Dashboard")
                    this.get_balances()
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
        get_balances() {
            this.balances.loading = true

            send_request({
                method: 'GET',
                url: this.$store.state.apiendpoints.product_get_balances.replace(":token", this.product.token),
            }).then(
                (res) => {
                    this.balances.data = res
                    this.balances.loading = false
                },
                () => {
                    this.$bvToast.toast('An Unknown Error Occurred while loading balances. Please Try Again!', {
                        ...this.$store.state.common_toast_options,
                        title: 'Error',
                        variant: 'danger'
                    })
                }
            )
        },
        do_withdraw(crypto) {
            this.withdrawl_form.active = true
            this.withdrawl_form.crypto = crypto
        },
        closePopup() {
            this.$bvToast.toast('Your withdraw request has been submitted, You will receive an update via email!', {
                ...this.$store.state.common_toast_options,
                title: 'Success',
                variant: 'success'
            })
            this.withdrawl_form.active = false
            this.withdrawl_form.crypto = null
        }
    }
}
</script>
