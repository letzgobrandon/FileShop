<template>
    <div>
        <b-sidebar 
            id="sidebar" 
            :title="null" 
            @shown="() => $store.dispatch('updateSidebarState', true)" 
            @hidden="() =>  $store.dispatch('updateSidebarState', false)" 
            :visible="$store.state.sidebar_visible"
            :no-header="!isMobile"
            width="240px"
            :backdrop="isMobile"
            :right="isMobile"
        >
            <div class="px-3 py-2">
                <h3 class="md:mt-3">About FileShop</h3>
                <p class="mt-4">
                    Fileshop is an open source marketplace to sell digital files.
                </p>
                <p>
                    You can host/fork your own version of fileshop having different features to earn income.
                </p>
                <a href="#" target="_blank">
                    <b-button 
                        pill
                        class="btn-theme"
                    >
                        <font-awesome-icon :icon="githubIcon" class="mr-1"/>
                        Fork GitHub
                    </b-button>
                </a>
                <a href="mailto:" class="ml-2">
                    <b-button 
                        pill
                        class="btn-theme"
                    >
                        <font-awesome-icon :icon="mailIcon" />
                    </b-button>
                </a>
            </div>
            <a id="sidebar-handle" slot="footer" href="#" @click.prevent="$store.dispatch('updateSidebarState', false)">
                <template v-if="$store.state.sidebar_visible">
                    <font-awesome-icon :icon="closeIcon" />
                </template>
            </a>
        </b-sidebar>
        <a id="sidebar-open" v-if="!$store.state.sidebar_visible" href="#" @click.prevent="$store.dispatch('updateSidebarState', true)">
            <font-awesome-icon :icon="openIcon" />
            ABOUT
        </a>
    </div>
</template>

<script>

import {faChevronLeft, faChevronRight } from "@fortawesome/free-solid-svg-icons"
import { faEnvelope } from "@fortawesome/free-regular-svg-icons"
import { faGithub } from "@fortawesome/free-brands-svg-icons"

export default {
    data() {
        return {
            isMobile: false
        }
    },
    computed: {
        openIcon: () => faChevronRight,
        closeIcon: () => faChevronLeft,
        githubIcon: () => faGithub,
        mailIcon: () => faEnvelope,
    },
    mounted() {
        this.checkIsMobile()
        window.addEventListener('resize', this.checkIsMobile)
    },
    methods: {
        checkIsMobile() {
            this.isMobile = window.innerWidth < 768
        }
    },
    beforeDestroy() {
        window.removeEventListener("resize", this.checkIsMobile)
    }
}
</script>