<template>
    <div>
        <b-form @submit.prevent="save">          
          <b-row class="text-left">
              <!-- Product Files -->
              <b-col cols="12" md="12">
                  <b-form-group class="files-container" :class="{'files-selected': files.length}">
                      <div class="file-top-text">
                          <img :src="require('@/assets/images/upload-icon.png')" />
                      </div>
                      <b-form-file 
                          multiple 
                          @input="filesChanged" 
                          id="files" 
                          v-model="files" 
                          placeholder="Upload Files to be Sold" 
                          required
                          :file-name-formatter="formatFileNames"
                          class="files-input"
                          :class="{'hide-label': files.length}"
                      ></b-form-file>
                      <div class="file-bottom-text">
                          <div v-if="files.length">
                              <ul class="files-info-container">
                                  <li v-for="(file, index) in files" :key="index" class="file-name-container">
                                      <span class="file-name">
                                          {{ file.name }}
                                      </span>
                                      <span class="file-action text-danger">
                                          <a href="#" class="text-danger" @click.prevent="removeFile(index)">X</a>
                                      </span>
                                  </li>
                              </ul>
                              <strong>Total Size: </strong> {{ files_stats.size || 0 }} MB / 5 MB
                          </div>
                          <div v-else>
                              maximum total size: 5 MB
                          </div>
                      </div>
                      <div class="text-danger" v-if="api_errors.files">
                          <small>{{ api_errors.files.join(",") }}</small>
                      </div>
                  </b-form-group>
              </b-col>
          </b-row>

          <b-row class="text-left">
              <!-- Product Name -->
              <b-col cols="12" md="8">
                  <b-form-group>
                      <b-form-input
                          id="product-name"
                          v-model="product.name"
                          placeholder="Product Name"
                          required
                          
                      ></b-form-input>
                      <div class="text-danger" v-if="api_errors.name">
                          <small>[[ api_errors.name.join(",") ]]</small>
                      </div>
                  </b-form-group>
              </b-col>
              
              <!-- Product Price -->
              <b-col cols="12" md="4">
                  <b-form-group>
                      <b-input-group>
                          <template #append>
                              <b-form-select
                                  :options="currency_options"
                                  v-model="product.currency"
                                  
                              ></b-form-select>
                          </template>
                          <b-form-input
                              id="product-price"
                              v-model="product.price"
                              placeholder="Price"
                              required
                              min="0"
                              type="number"
                              
                          ></b-form-input>
                      </b-input-group>
                  </b-form-group>
                  
                  <div class="text-danger" v-if="api_errors.price">
                      <small>[[ api_errors.price.join(",") ]]</small>
                  </div>
              </b-col>

          </b-row>
          
          <b-row class="text-left">
              <!-- Product Description -->
              <b-col cols="12" md="12">
                  <b-form-group>
                      <b-form-textarea
                          id="product-description"
                          v-model="product.description"
                          placeholder="Product Description"
                          rows="6"
                          max-rows="6"
                          
                      ></b-form-textarea>
                      
                      <div class="text-danger" v-if="api_errors.description">
                          <small>[[ api_errors.description.join(",") ]]</small>
                      </div>
                  </b-form-group>
              </b-col>
          </b-row>

          <!-- Submit Button -->
          <b-row class="mb-3">
              <b-col class="text-center">
                  <b-button pill type="submit" :disabled="submit_disabled" class="btn-theme">
                      Put up for Sale
                  </b-button>
              </b-col>
          </b-row>
        </b-form>
    </div>
</template>

<script>

import send_request from "../utils/requests"

export default {
    data() {
        return {
            product: {
            name: null,
            description: null,
            price: null,
            currency: 'USD'
            },
            files: [],
            files_stats: {},
            
            currency_options: [
            { value: 'USD', text: 'USD' },
            ],

            submit_disabled: false,
            api_errors: {},

            sidebar_visible: true
        }
    },
    mounted() {
      
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

            send_request({
                method: 'POST',
                url: this.$store.state.apiendpoints.product_create,
                data: payload,
                headers: {
                "Content-Type": "multipart/form-data"
                }
            }).then(
                (res) => {
                    this.submit_disabled = false
                    // window.location = this.$store.state.static_urls.email_update + `?uid=${res.uuid}&token=${res.token}`
                    this.$router.push({name: 'email-updates', query: {uid: res.uuid, token: res.token}})
                },
                (err) => {
                    this.submit_disabled = false
                    let response = err.response
                    if(response.status == 400) {
                        this.api_errors = response.data.error
                    } else {
                        this.$bvToast.toast('An Unknown Error Occurred. Please Try Again!', {
                        title: 'Error',
                        ...this.toast_options,
                        })
                    }
                }
            )
        },
        formatFileNames(files) {
            return files.length === 1 ? files[0].name : `${files.length} files selected`
        },
        removeFile(index) {
            this.files.splice(index, 1)
            this.filesChanged(this.files)
        }
    }
}
</script>

<style lang="scss">

.logo {
    font-family: 'Anton', sans-serif;
    font-size: 54px;
}

.about-carousel {
    .carousel-caption {
        color: #000;
    }
}

.step { 
    &--counter, &--label, &--details {
        text-align: center;
    }

    &--counter {
        margin-bottom: 0px;
        line-height: 0.9em;
        font-size: 4em;
    }

    &--label {
        text-transform: uppercase;
    }
}


.files-container {
    height: 180px;
    border: 2px dashed #242424;
    border-radius: 10px;
    transition: border-color 0.5s;
    overflow: hidden;
    
    &:hover {
        border-color: #6e3cff;
    }

    > div {
        height: 100%;
        background-color: #ddd;
        position: relative;
        width: 100%;;
    }

    .b-form-file {
        height: 100%;
        
        .custom-file-label {
            height: 100%;
            z-index: 5;
            position: absolute;
            display: flex !important;
            justify-content: center;
            align-items: center;
            background-color: transparent;
            
            .form-file-text {
                font-size: 1.5em;
                font-weight: 400;
                color: #000;
                opacity: 1;
                transition: opacity 0.5s;
            }

            &::after {
                height: 100%;
                content: '';
                width: 100%;
                left: 0;
                top: 0;
                border: 0;
                z-index: -1;
                background: transparent;
            }

        }

        &.hide-label {
            .custom-file-label {
                .form-file-text {
                    opacity: 0;
                }
            }
        }

    }

    .file-top-text  {
        position: absolute;
        top: 20px;
        bottom: 20px;
        text-align: center;
        width: 100%;
        height: calc(100%-40px);
        left: 0;

        img {
            height: 50px;
            transition: 0.5s all;
        }
    }
    .file-bottom-text  {
        position: absolute;
        top: 100px;
        text-align: center;
        width: 100%;
        left: 0;
        opacity: 1;
        transition: opacity 0.5s;
        z-index: 10;
        height: calc(100% - 100px);
        overflow: auto;
        
        &::-webkit-scrollbar {
            width: 7px;
        }

        &::-webkit-scrollbar-track {
            box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
        }

        &::-webkit-scrollbar-thumb {
            background-color: darkgrey;
            outline: 1px solid slategrey;
        }
    }
    
    &:not(.files-selected) {

        &:hover {
            .file-top-text {
                img {
                    height: 95%;
                }
            }

            .file-bottom-text {
                opacity: 0;
            }

            .b-form-file {
                .custom-file-label {
                    .form-file-text {
                        opacity: 0;
                    }
                }
            }
        }
    }

}

.files-info-container {
    list-style: none;
    text-align: center;
    padding: 0;
    margin: 0;
}
.file-name-container {
    display: flex;
    width: 100%;
    justify-content: center;
    align-items: center;
}
.file-action {
    margin-left: 10px;
    font-size: 0.55em;
    border-radius: 50%;
    border: 1px solid #DC3545;
    height: 1.5em;
    width: 1.5em;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 2px;
    text-decoration: none;
}
</style>