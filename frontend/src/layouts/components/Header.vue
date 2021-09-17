<template>
    <div :style="{paddingTop: headerPaddingAdjustment}" v-if="layout == 'main'" class="header layout--main">
        <b-row class="mt-4 text-center header-main" :class="{'sidebar-visible': $store.state.sidebar_visible}">
            <b-col cols="12">
                <router-link :to="{name: 'home'}">
                    <img class="logo mb-1" :src="require('@/assets/images/fs-logo-full.png')" />
                </router-link>
            </b-col>
            <b-col cols="12">
                <h5 class="logo-sub">Sell Files Anonymously for <span class="text-custom-orange">BTC</span> or <span class="text-custom-green">BCH!</span></h5>
            </b-col>
        </b-row>
        <b-row class="text-center m-0 header-mobile">
            <b-col cols="3">
                <router-link :to="{name: 'home'}">
                    <img class="logo mb-1" :src="require('@/assets/images/fs-logo.png')" />
                </router-link>
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
    <div :style="{paddingTop: headerPaddingAdjustment}" v-else-if="layout == 'sub'" class="header layout--sub">
        <b-row class="header-main w-100" :class="{'sidebar-visible': $store.state.sidebar_visible}">
            <b-col cols="12" md="2" class="text-center">
                <router-link :to="{name: 'home'}">
                    <img class="logo mb-1" :src="require('@/assets/images/fs-logo.png')" />
                </router-link>
            </b-col>
            <b-col cols="12" :md="$store.state.header.side ? 10 : 8" class="align-items-center d-flex justify-content-center">
                <h5 class="logo-sub text-center mx-auto">
                    {{ $store.state.header.title || "FileShop" }}
                </h5>
                <div class="logo-side">
                    <small>{{ $store.state.header.side }}</small>
                </div>
            </b-col>
            <b-col cols="12" md="2" v-if="!$store.state.header.side">
            </b-col>
        </b-row>
        <b-row class="text-center m-0 header-mobile" align="center">
            <b-col cols="3">
                <router-link :to="{name: 'home'}">
                    <img class="logo mb-1" :src="require('@/assets/images/fs-logo.png')" />
                </router-link>
            </b-col>
            <b-col cols="7" class="d-flex align-items-center justify-content-center">
                <h5 class="logo-sub">
                    {{ $store.state.header.title || "FileShop" }}
                </h5>
            </b-col>
            <b-col cols="2" class="d-flex align-items-center justify-content-center">
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
            layout: this.$route.meta && this.$route.meta.header ? this.$route.meta.header : 'main'
        }
    },
    computed: {
        menuIcon: () => faBars
    },
    watch: {
        $route(newV) {
            this.layout = newV.meta && newV.meta.header ? newV.meta.header : 'main'
        }
    },
    mounted() {
        this.checkIsMobile()
        window.addEventListener('resize', this.checkIsMobile)
    },
    methods: {
        checkIsMobile() {
            this.isMobile = window.innerWidth < 768
            if(this.isMobile) {
                this.headerPaddingAdjustment = document.querySelector(".header.layout--" + this.layout +" .header-mobile").clientHeight + "px"
            } else {
                if(this.layout == 'main')
                    this.headerPaddingAdjustment = 0
                else
                    this.headerPaddingAdjustment = 10 + 'px'
            }
        }
    },
    beforeDestroy() {
        window.removeEventListener("resize", this.checkIsMobile)
    }
}
</script>