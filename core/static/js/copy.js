var app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'], // Override Conflicting Delimiters because of DTL
    data: {
      toast_options: {
        autoHideDelay: 5000,
        appendToast: false,
        variant: 'success',
        toaster: 'b-toaster-bottom-center'
      },

      user_data: {
        email: current_email // Assumes it is present in scope
      },
  
      submit_disabled: false,
      api_errors: {},

      dashboard_url: null
    },
    mounted() {
      document.getElementById("preloader").style.top = "-120vh"
      setTimeout(() => {
        document.getElementById("preloader").style.display = "none"
      }, 2000)
    },
    methods: {
      copy(id) {
        const copyText = document.getElementById(id);
      
        /* Select the text field */
        copyText.select();
        copyText.setSelectionRange(0, 99999); /* For mobile devices */
      
        /* Copy the text inside the text field */
        document.execCommand("copy");
      
        this.$bvToast.toast('URL Copied Succesfully!', {
          title: 'Success',
          ...this.toast_options,
        })
      },
      save() {

        axios({
          method: 'POST',
          url: apiendpoints.product_seller_email_update,
          data: this.user_data,
          withCredentials: true
        }).then(
          (res) => {            
            this.dashboard_url = window.location.protocol + "//" + window.location.host + res.data.redirect_url
            this.$bvToast.toast("You'll be redirected to your Product Dashboard in 5 seconds", {
              ...this.toast_options,
              title: 'Success'
            })
            setTimeout(() => {
              window.location = res.data.redirect_url
            }, 5000)
          },
          (err) => {
            if(!err.response) {
              this.$bvToast.toast('A Network Error Occurred. Please check your internet connection and try Again.', {
                ...this.toast_options,
                title: 'Network Error',
                variant: 'danger'
              })
            } else {
              let response = err.response
              if(response.status == 400) {
                this.api_errors = response.data.error
                this.$bvToast.toast('Please fix the errors and try again', {
                  ...this.toast_options,
                  title: 'Error',
                  variant: 'danger'
                })
              } else {
                this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
                  ...this.toast_options,
                  title: 'Error',
                  variant: 'danger'
                })
              }
            }
            this.submit_disabled = false
          }
        )
      },
    }
  })
  Vue.use(window.BootstrapVue)
  