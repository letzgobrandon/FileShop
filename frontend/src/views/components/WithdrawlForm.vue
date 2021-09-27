<template>
    <div>
        <b-row class="text-left">
            <b-col cols="12" md="12" class="text-center">
                <b-form @submit.prevent="save">
                    <b-form-group
                        :label="'Enter your ' + crypto + ' Address to withdraw ' + amount"
                        label-for="address"
                    >
                        <b-form-input
                            id="address"
                            v-model="user_data.address"
                            placeholder="d78wr9wbvtycb9wtyvbc729atrvb92b"
                            required
                        ></b-form-input>
                        <div class="text-danger" v-if="api_errors.address">
                            <small>{{ api_errors.address.join(",") }}</small>
                        </div>
                    </b-form-group>
                    <b-button 
                        variant="primary" 
                        type="submit" 
                        :disabled="submit_disabled"
                    >
                        Place Withdrawl Request
                    </b-button>
                </b-form>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import send_request from '../../utils/requests'

export default {
    props: {
        product: {
            required: true,
            type: Object
        },
        crypto: {
            required: true,
            type: String
        },
        balances: {
            required: true,
            type: Object
        },
    },
    data() {
        return {
            user_data: {
                address: null,
            },
        
            submit_disabled: false,
            api_errors: {}
        }
    },
    computed: {
        amount() {
            if(!this.balances || !this.crypto) return 0
            return this.balances[this.crypto.toLowerCase()] || 0
        }
    },
    methods: {
        save() {
            this.submit_disabled = true
            send_request({
                method: 'POST',
                url: this.$store.state.apiendpoints.product_withdraw.replace(":token", this.product.token),
                data: {"address":  this.user_data.address, crypto:  this.crypto.toUpperCase()}
                }).then(
                    () => {
                        this.submit_disabled = false
                        this.$emit('success')
                    },
                (err) => {
                    
                    let response = err.response
                    if(response.status == 400) {
                        this.api_errors = response.data.error
                    } else {
                        this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
                            ...this.$store.state.common_toast_options,
                            title: 'Error',
                            variant: 'danger'
                        })
                    }
                    this.submit_disabled = false
                    this.$emit('failed')
                }
            )
        }
    }
}
</script>