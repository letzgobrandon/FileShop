<template>
    <div>
        <b-row class="text-left">
            <b-col cols="12" md="12" class="text-center">
                <b-form @submit.prevent="save">
                    <b-form-group
                        label-for="email"
                    >
                        <b-input-group> 
                            <template #append>
                                <b-button 
                                    variant="primary" 
                                    type="submit" 
                                    :disabled="submit_disabled"
                                >
                                    Save
                                </b-button>
                            </template>
                            <b-form-input
                                id="email"
                                v-model="user_data.email"
                                placeholder="Email"
                                required
                                type="email"
                            ></b-form-input>
                            <div class="text-danger" v-if="api_errors.name">
                                <small>{{ api_errors.name.join(",") }}</small>
                            </div>
                        </b-input-group>
                    </b-form-group>
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
        }
    },
    data() {
        return {
            user_data: {
                email: this.product.email,
            },
        
            submit_disabled: false,
            api_errors: {}
        }
    },
    mounted() {
        this.$store.dispatch('updateSidebarState', false) // Hide Sidebar
    },
    methods: {
        save() {
            this.submit_disabled = true
            send_request({
                method: 'PATCH',
                url: `${this.$store.state.apiendpoints.product_get}/${this.product.uid}`,
                data: {"token":  this.product.token, "email": this.user_data.email}
                }).then(
                    () => {
                        this.$bvToast.toast('Email Updated Successfully!', {
                            ...this.$store.state.common_toast_options,
                            title: 'Success',
                            variant: 'success'
                        })
                        this.submit_disabled = false
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
                }
            )
        }
    }
}
</script>