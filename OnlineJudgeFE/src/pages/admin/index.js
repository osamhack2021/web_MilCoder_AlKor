import i18n from '@/i18n';
import katex from '@/plugins/katex';
import store from '@/store';
import { GOOGLE_ANALYTICS_ID } from '@/utils/constants';

import filters from '@/utils/filters';
import 'babel-polyfill';
import Element from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import Vue from 'vue';
import VueAnalytics from 'vue-analytics';
import App from './App.vue';
import Cancel from './components/btn/Cancel.vue';
import IconBtn from './components/btn/IconBtn.vue';
import Save from './components/btn/Save.vue';

import Panel from './components/Panel.vue';
import router from './router';
import './style.less';

// register global utility filters.
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key]);
});

Vue.use(VueAnalytics, {
  id: GOOGLE_ANALYTICS_ID,
  router,
});
Vue.use(katex);
Vue.component(IconBtn.name, IconBtn);
Vue.component(Panel.name, Panel);
Vue.component(Save.name, Save);
Vue.component(Cancel.name, Cancel);

Vue.use(Element, {
  i18n: (key, value) => i18n.t(key, value),
});

Vue.prototype.$error = (msg) => {
  Vue.prototype.$message({ 'message': msg, 'type': 'error' });
};

Vue.prototype.$warning = (msg) => {
  Vue.prototype.$message({ 'message': msg, 'type': 'warning' });
};

Vue.prototype.$success = (msg) => {
  if (!msg) {
    Vue.prototype.$message({ 'message': 'Succeeded', 'type': 'success' });
  } else {
    Vue.prototype.$message({ 'message': msg, 'type': 'success' });
  }
};

new Vue(Vue.util.extend({ router, store, i18n }, App)).$mount('#app');
