<template>
    <b-form-group
        :label="label"
        :label-for="id"
        class="mb-0 custom-read-input"
    >
        <b-input-group>
            <template #append>
                <b-button variant="primary" :disabled="disabled" @click="do_copy()" v-if="copy">
                    <template v-if="!icon_only">Copy to Clipboard </template>
                    <font-awesome-icon :icon="copyIcon" />
                </b-button>
                <b-button variant="primary" :disabled="disabled" v-if="external">
                    <a :href="value" target="_blank" class="text-white">
                        <template v-if="!icon_only">Open </template>
                        <font-awesome-icon :icon="externalIcon" />
                    </a>
                </b-button>
            </template>
            <b-form-input
                :id="id"
                :value="display_value ? display_value : value"
                :placeholder="placeholder"
                readonly
                :class="{'variant-light': variant == 'light', 'text-center': text_center}"
            ></b-form-input>
        </b-input-group>
    </b-form-group>
</template>

<script>
import { faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons'
import { faCopy } from '@fortawesome/free-regular-svg-icons'
export default {
    props: {
        id: {
            required: true,
            type: String,
        },
        value: {
            required: false,
            type: String
        },
        display_value: {
            required: false,
            type: String
        },
        label: {
            required: false,
            type: String
        },
        placeholder: {
            required: false,
            type: String
        },
        disabled: {
            required: false,
            type: Boolean,
            default: false
        },
        copy: {
            required: false,
            default: false,
            type: Boolean
        },
        external: {
            required: false,
            default: false,
            type: Boolean
        },
        icon_only: {
            required: false,
            default: false,
            type: Boolean
        },
        variant: {
            required: false,
            type: String,
            default: 'normal',
        },
        text_center: {
            required: false,
            type: Boolean,
            default: false
        }
    },
    computed: {
        externalIcon: () => faExternalLinkAlt,
        copyIcon: () => faCopy
    },
    methods: {
        do_copy() {
            if(this.display_value)
                this.$copy_arbitary_text(this.value, this)
            else
                this.$copy_text(this.id, this)
        }
    }
}
</script>

<style lang="scss">
    @import "@/scss/colors";

    .custom-read-input {
        .variant-light {
            background-color: #fff;
            border-color: $primary-color !important;
            border-width: 2px;
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
        }
    }
</style>