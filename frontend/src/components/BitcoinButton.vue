<template>
    <a class="bitcoin-button" href="#" :class="{'btc': variant == 'btc', 'bch': variant == 'bch', 'no-right': hide_right}" @click="() => hide_right?false:$emit('input')">
        <div class="bitcoin-button--icon">
            <font-awesome-icon :icon="bitcoinIcon" size="2x" />
        </div>
        <div class="bitcoin-button--left">
            <template v-if="loading">
                <font-awesome-icon :icon="spinnerIcon" size="1x" spin />
            </template>
            <template v-else>
                {{ amount }}
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
            padding-left: 25px;
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
            background-color: #0ac18e;
        }
        &.btc:hover &--right{
            background-color: #bb7116;
        }
        &.bch:hover &--right{
            background-color: #08a176;
        }
    }
</style>