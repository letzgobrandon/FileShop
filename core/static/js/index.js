var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'], // Override Conflicting Delimiters because of DTL
  data: {
    product: {
      name: null,
      description: null,
      price: null,
      currency: 'USD'
    },
    files: [],
    files_stats: {},
    
    toast_options: {
      autoHideDelay: 5000,
      appendToast: false,
      variant: 'danger',
      toaster: 'b-toaster-bottom-center'
    },

    currency_options: [
      { value: 'USD', text: 'USD' },
    ],

    submit_disabled: false,
    api_errors: {}
  },
  mounted() {
    document.getElementById("preloader").style.top = "-120vh"
    setTimeout(() => {
      document.getElementById("preloader").style.display = "none"
    }, 2000)
  },
  methods: {
    filesChanged(files) {
      let val = "";
      let size = 0;
      
      files.forEach(file => {
        val += file.name;
        size += file.size;
        val += ", ";
      })
      
      val = val.slice(0,-2);
      size/=1000000;
      
      let obj = document.querySelector("#files")
      if(size>5){
        obj.setCustomValidity('Total size exceeds 5mb');
        obj.reportValidity();
      }
      else{
        obj.setCustomValidity('');
      }

      this.files_stats = {
        selected: val,
        size: size
      }

    },
    save() {

      let payload = new FormData()

      this.submit_disabled = true

      Object.keys(this.product).forEach(key => {
        payload.append(key, this.product[key])
      })

      this.files.forEach(v => {
        payload.append('files', v)
      })

      
      axios({
        method: 'POST',
        url: apiendpoints.product_create,
        data: payload,
        withCredentials: true,
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }).then(
        (res) => {
          this.submit_disabled = false
          window.location = res.data.redirect_url
        },
        (err) => {
          if(!err.response) {
            this.$bvToast.toast('A Network Error Occurred. Please check your internet connection and try Again.', {
              ...this.toast_options,
              title: 'Network Error'
            })
          } else {
            let response = err.response
            if(response.status == 400) {
              this.api_errors = response.data.error
              this.$bvToast.toast('Please fix the errors and try again', {
                title: 'Error',
                ...this.toast_options,
              })
            } else {
              this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
                title: 'Error',
                ...this.toast_options,
              })
            }
          }
          this.submit_disabled = false
        }
      )
    },
    formatFileNames(files) {
      return files.length === 1 ? files[0].name : `${files.length} files selected`
    }
  }
})
Vue.use(window.BootstrapVue)
