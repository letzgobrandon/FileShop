<template>
    <div>
        <b-table
            :fields="fields"
            :items="results" 
            :busy="loading" 
            class="mt-3 text-center" 
            outlined
            sticky-header
            show-empty
            empty-text="No entries yet. Share you product and start selling."
            empty-filtered-text="No entries yet. Share you product and start selling."
        >
            <template #table-busy>
                <div class="text-center text-primary my-2">
                    <b-spinner class="align-middle"></b-spinner>
                    <strong class="d-block">Loading</strong>
                </div>
            </template>

            <!-- ID -->
            <template #cell()="data">
                {{ data.index + 1 }}
            </template>

            <!-- Timestamp -->
            <template #cell(timestamp)="data">
                {{ formatDate(data.item.timestamp) }}
            </template>

            <!-- Txid -->
            <template #cell(txid)="data">
                {{ data.item.txid || "N/A" }}
            </template>

            <!-- Status -->
            <template #cell(status_of_transaction)="data">
                <b-badge pill :variant="badge_colors[data.item.status_of_transaction]">
                    {{ status_options[data.item.status_of_transaction] }}
                </b-badge>
            </template>

            <!-- Payment Status -->
            <template #cell(is_payment_complete)="data">
                    <template v-if="data.item.is_payment_complete">
                        <font-awesome-icon :icon="checkIcon" class="text-success" />
                        <br/>
                        <small>Received</small>
                    </template>
                    <template v-else-if="data.item.received_value">
                        <font-awesome-icon :icon="warningIcon" class="text-warning" />
                        <br/>
                        <small>
                            {{ data.item.received_value }} Received
                        </small>
                    </template>
                    <template v-else>
                        <font-awesome-icon :icon="dangerIcon" class="text-danger" />
                        <br/>
                        <small>Not Received</small>
                    </template>
            </template>

            <!-- Amount -->
            <template #cell(expected_value)="data">
                {{ data.item.expected_value }} {{ data.item.crypto }}
            </template>

        </b-table>
        <b-pagination
            v-model="current_page"
            :total-rows="total_results"
            :per-page="this.filters.limit"
            size="sm"
            pills
            align="center"
            v-if="total_results > filters.limit"
        ></b-pagination>
    </div>
</template>

<script>
import { faCheckCircle, faExclamationTriangle, faTimesCircle } from '@fortawesome/free-solid-svg-icons'
import send_request from '../../utils/requests'
export default {
    props: {
        product: {
            required: true,
            type: Object
        }
    },
    data() {
        return {
            fields: [
                { key: 'id', label: '#', class: 'text-center' },
                { key: 'timestamp', label: 'Date', class: 'text-center' },
                { key: 'txid', label: 'Tx ID', class: 'text-center' },
                { key: 'status_of_transaction', label: 'Status', class: 'text-center' },
                { key: 'is_payment_complete', label: 'Payment', class: 'text-center' },
                { key: 'expected_value', label: 'Amount', class: 'text-center'},
            ],
            status_options: {
                "-1": 'Not Started',
                "0": "Unconfirmed",
                "1": "Partially Confirmed",
                "2": "Confirmed",
            },
            badge_colors: {
                "-1": 'dark',
                "0": "danger",
                "1": "warning",
                "2": "success",
            },
            results: [],
            loading: true,

            total_results: 0,
            current_page: 1,

            filters: {
                offset: 0,
                limit: 20
            }
        }
    },
    computed: {
        checkIcon: () => faCheckCircle,
        warningIcon: () => faExclamationTriangle,
        dangerIcon: () => faTimesCircle,  
    },
    watch: {
        current_page(newV, oldV) {
            if(newV == oldV) return
            this.filters.offset = this.filters.limit * (newV - 1)
            this.load_data()
        }
    },
    mounted() {
        this.load_data()
    },
    methods: {
        load_data() {
            this.loading = true
            send_request({
                method: 'GET',
                url: this.$store.state.apiendpoints.product_get_orders.replace(":token", this.product.token),
                params: this.filters
            }).then(
                (res) => {
                    this.results = res.results
                    this.loading = false
                    this.total_results = res.count
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
        formatDate(date) {
            date = new Date(date)

            let day = date.getDate();
            if(day.toString().length < 2)
                day = "0" + day
            
            let month = date.getMonth() + 1
            if(month.toString().length < 2)
                month = "0" + month
            
            let year = date.getFullYear();
            
            return `${day}.${month}.${year}`;  
        }
    }
}
</script>

<style lang="scss">
    .b-table-sticky-header {
        max-height: 100vh;
    }
</style>