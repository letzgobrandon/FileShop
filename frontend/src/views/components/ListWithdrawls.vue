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
            <template #cell(uid)="data">
                <div v-b-popover.hover="{variant: 'primary', content: data.item.uid || 'No Data Available'}">
                    {{ (data.item.uid ? data.item.uid.substring(0, 8) + "..." : null) || "N/A" }}
                </div>
            </template>

            <!-- Timestamp -->
            <template #cell(created_on)="data">
                <div v-b-popover.hover="{variant: 'primary', content: 'Last Updated On ' + formatDate(data.item.modified_on)}">
                    {{ formatDate(data.item.created_on) }}
                </div>
            </template>

            <!-- Txid -->
            <template #cell(txid)="data">
                {{ data.item.txid || "N/A" }}
            </template>

            <!-- Status -->
            <template #cell(status)="data">
                <b-badge pill :variant="badge_colors[data.item.status]">
                    {{ status_options[data.item.status] }}
                </b-badge>
            </template>

            <!-- Amount -->
            <template #cell(amount)="data">
                <div v-b-popover.hover="{variant: 'info', html: true, content: '<strong>Address:</strong> ' + data.item.address}">
                    {{ data.item.amount }} {{ data.item.crypto }}
                </div>
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
                { key: 'uid', label: 'Request ID', class: 'text-center' },
                { key: 'created_on', label: 'Date', class: 'text-center' },
                { key: 'txid', label: 'Tx ID', class: 'text-center' },
                { key: 'status', label: 'Status', class: 'text-center' },
                { key: 'amount', label: 'Amount', class: 'text-center'},
            ],
            status_options: {
                "p": 'Pending',
                "i": "Initiated",
                "c": "Completed",
                "r": "Rejected",
            },
            badge_colors: {
                "p": 'dark',
                "i": "warning",
                "c": "success",
                "r": "danger",
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
                url: this.$store.state.apiendpoints.product_get_withdrawls.replace(":token", this.product.token),
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