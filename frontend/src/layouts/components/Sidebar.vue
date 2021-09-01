<template>
    <div>
        <b-sidebar 
            id="sidebar" 
            title="Sidebar" 
            @shown="() => $store.dispatch('updateSidebarState', true)" 
            @hidden="() =>  $store.dispatch('updateSidebarState', false)" 
            :visible="$store.state.sidebar_visible"
            :no-header="true"
            width="240px"
        >
            <div class="px-3 py-2">
                <b-img :src="require('@/assets/images/fs-logo.png')" fluid class="sidebar-logo"></b-img>
                <hr class="sidebar-seperator mx-auto" />
                <ul class="sidebar-list">
                    <li class="sidebar-list-item">
                        <a href="#">About</a>
                    </li>
                </ul>
            </div>
            <div id="sidebar-handle" slot="footer">
                <template v-if="$store.state.sidebar_visible">
                    <a href="#" @click.prevent="$store.dispatch('updateSidebarState', false)">
                        <font-awesome-icon :icon="closeIcon" />
                    </a>
                </template>
            </div>
        </b-sidebar>
        <div id="sidebar-open" v-if="!$store.state.sidebar_visible">
            <a href="#" @click.prevent="$store.dispatch('updateSidebarState', true)">
                <font-awesome-icon :icon="openIcon" />
                OPEN
            </a>
        </div>
    </div>
</template>

<script>

import {faChevronLeft, faChevronRight } from "@fortawesome/free-solid-svg-icons"

export default {
    computed: {
        openIcon: () => faChevronRight,
        closeIcon: () => faChevronLeft,
    }
}
</script>