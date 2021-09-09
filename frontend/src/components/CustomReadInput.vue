<template>
    <b-form-group
        :label="label"
        :label-for="id"
        class="mb-0"
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
                :value="value"
                :placeholder="placeholder"
                readonly
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
        }
    },
    computed: {
        externalIcon: () => faExternalLinkAlt,
        copyIcon: () => faCopy
    },
    methods: {
        do_copy() {
            this.$copy_text(this.id, this)
        }
    }
}
</script>