<template>
    <div>
        <b-row v-if="loading" class="py-4">
            <b-col>
                <h5 class="text-center">Loading.. Please wait..</h5>
            </b-col>
        </b-row>
        <b-row no-gutters v-else>
            <template v-if="order.status_of_transaction == 2">
                <b-col xs="12" md="12" xl="12">
                    <b-col cols="12" md="12">
                        <img class="card-img-top" :src="require('@/assets/images/product_placeholder.png')" alt="Card Image Cap">
                    </b-col>
                    <b-col cols="12" md="12" class="px-4 py-2">
                        <h5 class="card-title">
                            {{ order.product.name || "No Name" }}
                        </h5>
                        <p class="card-text">
                            {{ order.product.product_description || "No Description" }}
                        </p>
                        <p class="d-flex align-items-center">
                            <strong>Total files: </strong> 
                            {{ order.product.num_files || 0 }}
                            <a :href="download_url" target="_blank">
                                <b-button size="sm" class="ml-3">Download Files</b-button>
                            </a>
                        </p>
                        <p class="text-left">
                            <b-form-group
                                label="Save the link below to come back to this page:"
                                label-for="order-url"
                            >
                                <b-input-group>
                                    <template #append>
                                        <b-button variant="info" @click="copy('order-url')">
                                            Copy to Clipboard
                                            <img id="copy-content" :src="require('@/assets/images/copy_white.png')" width=20px height=20px alt="Copy to clipboard">
                                        </b-button>
                                    </template>
                                    <b-form-input
                                        id="order-url"
                                        :value="public_url"
                                        placeholder="Public URL"
                                        readonly
                                    ></b-form-input>
                                </b-input-group>
                            </b-form-group>
                        </p>
                    </b-col>
                    <b-col cols="12" md="12" class="px-4 py-2 text-left d-flex">

                    </b-col>
                </b-col>
            </template>
            <template v-else>
                <b-col xs="12" md="12" xl="12" class="text-center mx-auto">
                    <h3>Error</h3>
                    <p>This order is still pending Payment.</p>
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
        
            submit_disabled: false,
            api_errors: {},
            loading: true
        }
    },
    computed: {
        public_url() {
            return `${window.location.protocol}//${window.location.host}${this.$route.path}`
        },
        download_url() {
            if(!this.order) return ""
            return this.$store.state.static_urls.download_url.replace(":order_uid", this.order.uid)
        }
    },
    mounted() {
        console.log(this.$route)
        this.$store.dispatch('updateSidebarState', false)

        this.order_uid = this.$route.params.order_uid

        if(this.order_uid)
            this.load_data()

        this.$store.dispatch("updateSiteTitle", "View Order")
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
            this.loading = false
        },
        copy(id) {
            this.$copy_text(id, this)
        }
    }
}
</script>