<template>
    <div>
        <Header />
        <b-container :class="{'sidebar-visible': $store.state.sidebar_visible}">
            <Sidebar />
            <b-row>
                <b-col :cols="cols.xs" :md="cols.md" class="mx-auto">
                    <b-row class="overflow-hidden mt-4">
                        <b-col cols="12" md="12" class="px-4 py-2">
                            <router-view></router-view>
                        </b-col>
                    </b-row>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import Header from "./components/Header.vue"
import Sidebar from "./components/Sidebar.vue"

export default {
    components: {
        Header,
        Sidebar
    },
    computed: {
        cols() {
            let default_cols = {
                xs: 12,
                md: 8
            }
            if(this.$route.meta && this.$route.meta.layout && this.$route.meta.layout.cols) {
                default_cols = {
                    ...default_cols,
                    ...this.$route.meta.layout.cols
                }
            }
            return default_cols
        }
    }
}
</script>