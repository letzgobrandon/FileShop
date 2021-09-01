<template>
    <div>
        <b-row no-gutters>
            <b-col cols="12" md="12" class="px-4 py-2 text-center">
                <h3>Your Product is now live!</h3>
                <b-row class="text-left">
                    <b-col cols="12" md="12" class="text-center">
                        <b-form-group
                            label="Public URL"
                            label-for="product-url"
                        >
                            <b-input-group>
                                <template #append>
                                    <b-button variant="info" :disabled="submit_disabled" @click="copy('product-url')">
                                        Copy to Clipboard
                                        <img id="copy-content" :src="require('@/assets/images/copy_white.png')" width=20px height=20px alt="Copy to clipboard">
                                    </b-button>
                                </template>
                                <b-form-input
                                    id="product-url"
                                    :value="public_url"
                                    placeholder="Public URL"
                                    readonly
                                ></b-form-input>
                            </b-input-group>
                        </b-form-group>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
        <b-row no-gutters class="mb-4">
            <b-col class="px-4 py-2">
                <b-form @submit.prevent="save">
                    <b-row class="text-left">
                        <!-- Product Name -->
                        <b-col cols="12" md="12" class="text-center">
                            <b-form-group
                                label="Enter your email address to receive updates on orders or to withdraw received funds"
                                label-for="email"
                            >
                                <b-input-group> 
                                    <template #append>
                                        <b-button 
                                            variant="info" 
                                            type="submit" 
                                            :disabled="submit_disabled"
                                        >
                                            Send Mail
                                        </b-button>
                                    </template>
                                    <b-form-input
                                        id="email"
                                        v-model="user_data.email"
                                        placeholder="e.g. username@example.com"
                                        required
                                        type="email"
                                    ></b-form-input>
                                    <div class="text-danger" v-if="api_errors.name">
                                        <small>{{ api_errors.name.join(",") }}</small>
                                    </div>
                                </b-input-group>
                            </b-form-group>
                        </b-col>
                    </b-row>
                </b-form>
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
            product_token: null,
            user_data: {
                email: null,
            },
        
            submit_disabled: true,
            api_errors: {},

            dashboard_url: null
        }
    },
    computed: {
        public_url() {
            if(!this.product_uid) return null

            return window.location.protocol + "//" + window.location.host + "/product/" + this.product_uid
        }
    },
    mounted() {
        this.$store.dispatch('updateSidebarState', false) // Hide Sidebar
        this.get_data()
    },
    methods: {
        get_data() {
            this.product_uid = this.$route.query.uid
            this.product_token = this.$route.query.token
            this.submit_disabled = false
        },
        save() {
            send_request({
                method: 'PATCH',
                url: `${this.$store.state.apiendpoints.product_get}/${this.product_uid}`,
                data: {"token":  this.product_token, "email": this.user_data.email}
                }).then(
                    () => {
                        this.$bvToast.toast('Saved', {
                            ...this.toast_options,
                            title: 'Success',
                            variant: 'success'
                        })
                        // this.dashboard_url = window.location.protocol + "//" + window.location.host + "/" + static_urls.seller_dashboard.replace(":token", this.product_token)
                        // window.location.href = this.dashboard_url
                        // this.$router.push({name: 'seller-dashboard', query: {token: }})
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
            this.$copy_text(id, this)
        }
    }
}
</script>