export default {
    updateSidebarState({commit}, value) {
        commit('UPDATE_SIDEBAR_STATE', value)
    },
    updateSiteTitle(t, value) {
        document.title = `${value} | FileShop`
    }
}