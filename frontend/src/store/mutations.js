export default {
    UPDATE_SIDEBAR_STATE(state, value) {
        state.sidebar_visible = value
    },
    UPDATE_HEADER_TITLE(state, value) {
        state.header.title = value
    },
    UPDATE_HEADER_SIDE(state, value) {
        state.header.side  = value
    },
    SET_SERVICE_WORKER(state, registration) {
        state.active_service_worker = registration
    },
}