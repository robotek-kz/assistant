import Vue from 'vue';
import VueSocketIOExt from 'vue-socket.io-extended';
import io from 'socket.io-client';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { far } from '@fortawesome/free-regular-svg-icons';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';
// import VueTour from 'vue-tour';
import App from './App.vue';
import router from './router';
import store from './store';
import Modal from '@/components/Modal.vue';
import VTooltip from 'v-tooltip'
import simplebar from "simplebar-vue";
import "simplebar/dist/simplebar.min.css";



import vClickOutside from 'v-click-outside';
let eventHub = new Vue();
Vue.component("simplebar", simplebar);
Vue.use(vClickOutside);
Vue.use(VTooltip)
let FileUploadComponent = Vue.extend({
    template: '<div class="{{ class }}"><label for="{{ name }}"><input type="file" name="{{ name }}" id="{{ id || name }}" accept="{{ accept }}" v-on:click="fileInputClick" v-on:change="fileInputChange" multiple="{{ multiple }}"><slot></slot></label><button type="button" v-on:click="fileUpload">{{ buttonText }}</button></div>',
    props: {
        class: String,
        name: {
            type: String,
        },
        id: String,
        action: {
            type: String,
        },
        accept: String,
        multiple: String,
        headers: Object,
        method: String,
        buttonText: {
            type: String,
            default: 'Upload'
        }
    },
    data() {
        return {
            myFiles: []
        }
    },
    methods: {
        fileInputClick() {
            eventHub.$emit('onFileClick', this.myFiles)
        },
        fileInputChange() {
            var ident = this.id || this.name
        },
        _onProgress(e) {

        },
        _handleUpload(file) {
            this.$dispatch('beforeFileUpload', file);
            let form = new FormData();
            let xhr = new XMLHttpRequest();
        },
        fileUpload() {

        }

    }
})

Vue.component('file-upload', FileUploadComponent)

Vue.filter('prettyBytes', (num) => {
    if (typeof num !== 'number' || isNaN(num)) {
        throw new TypeError('Expected a number');
    }

    let exponent;
    let unit;
    let neg = num < 0;
    let units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB'];

    if (neg) {
        num = -num;
    }

    if (num < 1) {
        return (neg ? '-' : '') + num + ' B';
    }

    exponent = Math.min(Math.floor(Math.log(num) / Math.log(1000)), units.length - 1);
    num = (num / Math.pow(1000, exponent)).toFixed(2) * 1;
    unit = units[exponent];

    return (neg ? '-' : '') + num + ' ' + unit;
});
const install = function (Vue, options) {
    Vue.component('vue-modal', Modal);

    Vue.prototype.$modals = {
        /**
         * Modals that are currently shown.
         *
         * @var array
         */
        shownModals: new Array(),

        /**
         * All modals loaded to the view app.
         *
         * @var array
         */
        allModals: new Array(),

        /**
         * Shows a named modal.
         *
         * @param string modalName
         *
         * @return void
         */
        show: function (modalName) {
            this.shownModals.indexOf(modalName) == -1 ? this.shownModals.push(modalName) : null;
            if (options && options.logging) {
                console.log('Show modal: ' + modalName);
                console.log('All modals showing: ', this.shownModals);
            }
        },

        /**
         * Hides a named modal.
         *
         * @param string| array modalNames
         *
         * @return void
         */
        hide: function (modalNames) {
            /* Removes the scroll lock */
            document.body.classList.remove('v-modal__no-scroll');

            if (modalNames.constructor === Array) {
                var _this = this;
                modalNames.forEach(function (modalName) {
                    var ind = _this.shownModals.indexOf(modalName);
                    _this.shownModals.splice(ind, 1);
                });
            } else {
                var ind = this.shownModals.indexOf(modalNames);
                this.shownModals.splice(ind, 1);
            }
            if (options && options.logging) {
                console.log('Removed modal: ' + modalNames);
                console.log('All shown modals: ', this.shownModals);
            }
        },

        /**
         * Determines if a modal should be shown or not.
         *
         * @param string modalName
         *
         * @return boolean
         */
        isActive: function (modalName) {
            return this.shownModals.indexOf(modalName) > -1;
        },

        /**
         * Return all modals that are currently shown.
         *
         * @return array
         */
        shown: function () {
            return this.shownModals;
        },

        /**
         * Return all modals bound to the current Vue context.
         *
         * @return array
         */
        all: function () {
            return this.allModals;
        },

        /**
         * Mount a new modal to the state.
         *
         * @return null
         */
        mount: function (name) {
            if (this.allModals.indexOf(name) == -1) {
                this.allModals.push(name);
            } else if (options && options.logging) {
                console.log('The modal name "' + name + '" has already been mounted.');
            }
        }

    }
}
install(Vue);
// require('vue-tour/dist/vue-tour.css');
// import trackMouse from './trackMouse';

// Vue.mixin(trackMouse);

const socket = io(process.env.VUE_APP_URL, {
  autoConnect: false,
  reconnectionAttempts: 3,
  timeout: 10000,
});

library.add(fas, far, fab);

Vue.use(VueSocketIOExt, socket, { store });
// Vue.use(VueTour);
Vue.component('fa', FontAwesomeIcon);
Vue.config.productionTip = false;
router.beforeEach((to, from, next) => Promise.all([store.dispatch('user/checkAuth')]).then(next));
new Vue({
  router,
  store,
  render(h) { return h(App); },
}).$mount('#app');

window.addEventListener('message', (e) => {
  if (e.data && e.data.type === 'webpackInvalid') {
    console.clear();
  }
});

console.blue = (msg) => {
  console.log(`%c${msg}`, 'color: #00cdff');
};
console.green = (msg) => {
  console.log(`%c${msg}`, 'color: #00dd00');
};
