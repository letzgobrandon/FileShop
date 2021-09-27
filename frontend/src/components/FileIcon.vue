<template>
    <span class="file-icon">
        <font-awesome-icon :icon="fileIcon" />
        <span :style="'background-color: ' + color_maps[icon] || '#000' + ';'">{{ icon || "?" }}</span>
    </span>
</template>

<script>
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons';
import { faFile } from '@fortawesome/free-regular-svg-icons';
export default {
    props: {
        name: {
            required: true,
            type: String
        }
    },
    data() {
        return {
            color_maps: {
                'jpeg': '#f2994a',
                'jpg': '#f2994a',
                'png': '#f2994a',
                'gif': '#f2994a',

                'pdf': '#eb5757',

                'xls': '#27AE60',
                'xlsx': '#27AE60',

                'ppt': '#2D9CDB',
                'pptx': '#2D9CDB',

                'doc': '#00A4EF',
                'docx': '#00A4EF',

                'exe': '#F25022',
                'zip': '#737373'

            }
        }
    },
    computed: {
        icon () {
            if(!this.name) return this.unknownFileIcon
            
            let extension = this.name.split(".").slice(-1)[0]
            return  extension
            // let icon = this.icon_maps[extension]
            // if(!icon) return this.unknownFileIcon

            // return icon
        },
        unknownFileIcon: () => faQuestionCircle,
        fileIcon: () => faFile
    }
}
</script>

<style lang="scss">
    .file-icon {
        position: relative;

        .svg-inline--fa {
            font-size: 2.5em;
        }
        span {
            position: absolute;
            left: -10px;
            bottom: 4px;
            background-color: #000;
            color: #fff;
            font-size: 0.7em;
            font-weight: bold;
            padding: 2px;
            text-transform: uppercase;
        }
    }
</style>