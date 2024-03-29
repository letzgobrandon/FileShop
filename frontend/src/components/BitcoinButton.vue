<template>
    <a 
        class="bitcoin-button" 
        href="#" 
        :class="{'btc': variant == 'btc', 'bch': variant == 'bch', 'no-right': hide_right, 'disabled': disabled, 'left-disabled': disable_amount}" 
        @click.prevent="() => hide_right || disabled ?false:$emit('input')"
    >
        <div class="bitcoin-button--icon">
            <font-awesome-icon :icon="bitcoinIcon" size="2x" />
        </div>
        <div class="bitcoin-button--left" v-if="!disable_amount">
            <template v-if="loading">
                <font-awesome-icon :icon="spinnerIcon" size="1x" spin />
            </template>
            <template v-else>
                <template v-if="show_approx">&thickapprox;</template> {{ amount }} <template v-if="show_symbol">{{ variant.toUpperCase() }}</template>
            </template>
        </div>
        <div class="bitcoin-button--right" v-if="!hide_right">
            {{ label }}
        </div>
    </a>
</template>

<script>
import { faBitcoin } from '@fortawesome/free-brands-svg-icons'
import { faSpinner } from '@fortawesome/free-solid-svg-icons'
export default {
    props: {
        variant: {
            required: false,
            type: String,
            default: 'btc'
        },
        amount: {
            required: true,
            type: Number,
            default: 0
        },
        label: {
            required: true,
            type: String,
            default: "withdraw"
        },
        hide_right: {
            required: false,
            type: Boolean,
            default: false
        },
        loading: {
            required: false,
            type: Boolean,
            default: false
        },
        disabled: {
            required: false,
            type: Boolean,
            default: false
        },
        disable_amount: {
            required: false,
            type: Boolean,
            default: false
        },
        show_approx: {
            required: false,
            type: Boolean,
            default: true
        },
        show_symbol: {
            required: false,
            type: Boolean,
            default: true
        }
    },
    computed: {
        bitcoinIcon: () => faBitcoin,
        spinnerIcon: () => faSpinner
    }
}
</script>

<style lang="scss">
    .bitcoin-button {
        height: 40px;
        position: relative;
        display: inline-flex;
        align-items: center;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #fff;
        font-weight: 500;
        padding-left: 20px;
        cursor: pointer;
        text-decoration: none;

        &--icon {
            position: absolute;
            left: 0;
            top: 0;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            color: #fff;
            overflow: hidden;
            box-shadow: 10px 0 15px 1px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        &--right, &--left {
            background-color: #f7931a;
            height: 40px;
            display: inline-flex;
            align-items: center;
            padding-right: 8px;
            padding-left: 8px;
            transition: 0.3s all;
        }
        &--left {
            padding-left: 30px;
            min-width: 100px;
            text-align: right;
            justify-content: flex-end;
        }

        &.no-right &--left {
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
        }

        &--right {
            margin-left: 2px;
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
        }

        &.left-disabled &--right {
            padding-left: 30px;
        }

        &:hover, &:focus {
            text-decoration: none;
            color: #fff;
        }

        &.btc &--icon,
        &.btc &--right, 
        &.btc &--left  {
            background-color: #f7931a;
        }
        &.bch &--icon,
        &.bch &--right, 
        &.bch &--left {
            background-color: #08a176;
        }
        &.btc:hover &--right{
            background-color: #bb7116;
        }
        &.bch:hover &--right{
            background-color: #08a176;
        }
        &.btc.disabled {
            cursor: not-allowed;
        }
        &.btc.disabled &--icon,
        &.btc.disabled &--right, 
        &.btc.disabled &--left  {
            background-color: #f5b86e;
        }
        &.bch.disabled {
            cursor: not-allowed;
        }
        &.bch.disabled &--icon,
        &.bch.disabled &--right, 
        &.bch.disabled &--left  {
            background-color: #62bea4;
        }
    }
</style>