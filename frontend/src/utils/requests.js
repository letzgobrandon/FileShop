import Axios from "axios"
import state from "../store/state"

export default function send_request({
    url=null,
    method=null,
    data=null,
    params=null,
    headers=null,
    with_credentials=true,
    vue_instance=null
}={}) {

    return new Promise((resolve, reject) => {

        Axios({
            method: method,
            url: url,
            data: data,
            params: params,
            headers: headers,
            withCredentials: with_credentials
          }).then(
            (res) => {
                resolve(res.data)
            },
            (err) => {
                if(!err.response) {
                    if(vue_instance) {
                        vue_instance.$bvToast.toast('A Network Error Occurred. Please check your internet connection and try Again.', {
                            ...state.common_toast_options,
                            title: 'Network Error',
                            variant: 'danger'
                        })
                    }
                    reject(err)
                } else {
                    let response = err.response
                    if(response.status == 400 && vue_instance) {
                        vue_instance.$bvToast.toast('Please fix the errors and try again', {
                            ...state.common_toast_options,
                            title: 'Error',
                            variant: 'danger'
                        })
                    }
                    reject(err)
                }
            }
        )
    })
}