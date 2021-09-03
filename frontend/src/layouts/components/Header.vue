<template>
    <div :style="{paddingTop: headerPaddingAdjustment}">
        <b-row class="mt-4 text-center" id="header" :class="{'sidebar-visible': $store.state.sidebar_visible}">
            <b-col cols="12">
                <img class="logo mb-1" :src="require('@/assets/images/fs-logo-full.png')" />
            </b-col>
            <b-col cols="12">
                <h5 class="logo-sub">Sell Files Anonymously for <span class="text-custom-orange">BTC</span> or <span class="text-custom-green">BCH!</span></h5>
            </b-col>
        </b-row>
        <b-row class="text-center m-0" id="header-mobile">
            <b-col cols="3">
                <img class="logo mb-1" :src="require('@/assets/images/fs-logo.png')" />
            </b-col>
            <b-col cols="7">
                <h5 class="logo-sub">Sell Files Anonymously for <span class="text-custom-orange">BTC</span> or <span class="text-custom-green">BCH!</span></h5>
            </b-col>
            <b-col cols="2">
                <a href="#" @click.prevent="$store.dispatch('updateSidebarState', true)" class="menu-button">
                    <font-awesome-icon :icon="menuIcon"/>
                </a>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import { faBars } from '@fortawesome/free-solid-svg-icons'
export default {
    data() {
        return {
            headerPaddingAdjustment: 0,
            isMobile: false,
        }
    },
    computed: {
        menuIcon: () => faBars
    },
    mounted() {
        this.checkIsMobile()
        window.addEventListener('resize', this.checkIsMobile)
    },
    methods: {
        checkIsMobile() {
            this.isMobile = window.innerWidth < 768
            if(this.isMobile) {
                this.headerPaddingAdjustment = document.getElementById("header-mobile").clientHeight + "px"
            } else {
                this.headerPaddingAdjustment = 0
            }
        }
    },
    beforeDestroy() {
        window.removeEventListener("resize", this.checkIsMobile)
    }
}
</script>