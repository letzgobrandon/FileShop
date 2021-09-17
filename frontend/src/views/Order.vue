<template>
    <div>
        <b-row v-if="loading" class="py-4">
            <b-col>
                <h5 class="text-center">Loading.. Please wait..</h5>
            </b-col>
        </b-row>
        <b-row no-gutters v-else>
            <template v-if="order.status_of_transaction > -1 && order.is_payment_complete">
                <b-alert show variant="success" class="mx-auto">
                    <font-awesome-icon :icon="checkCircleIcon" class="mr-2" /> Payment Successful
                </b-alert>
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
                                <b-tr v-for="(data, index) in order.product.files" :key="index">
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
                        <b-col cols="12" md="6" class="text-center">
                            <h5 class="card-title text-underline">
                                Total Files
                            </h5>
                            <h5>
                                <template v-if="loading">
                                    Loading...
                                </template>
                                <template v-else>
                                    {{ order.product.num_files || 0 }}
                                </template>
                            </h5>
                        </b-col>
                        <b-col cols="12" md="6" class="text-center">
                            <h5 class="card-title text-underline">
                                Total Size
                            </h5>
                            <h5>
                                <BytesToHuman :bytes="order.product.files.reduce((p, c) => p + c.file_size, 0)" />
                            </h5>
                        </b-col>
                    </b-row>
                </b-col>
                <b-col cols="12" md="12" class="px-4 py-2 text-center">
                    <a :href="download_url" target="_blank">
                        <b-button pill variant="primary" class="font-weight-bold">
                            <font-awesome-icon :icon="downloadIcon" class="mr-2"/>
                            Download Files
                        </b-button>
                    </a>
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

import BytesToHuman from "@/components/BytesToHuman"
import FileIcon from "@/components/FileIcon"
import { faCheckCircle, faDownload } from '@fortawesome/free-solid-svg-icons'

export default {
    components: {
        BytesToHuman,
        FileIcon
    },
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
        },
        checkCircleIcon: () => faCheckCircle,
        downloadIcon: () => faDownload
    },
    mounted() {
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
            this.$store.dispatch('updateHeaderTitle', this.order.product.product_name)
            this.$store.dispatch('updateHeaderSide', `Order #${this.order.uid}`)
            
            this.loading = false
        },
        copy(id) {
            this.$copy_text(id, this)
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