import i18n from '@/i18n';

import highlight from '@/plugins/highlight';
import katex from '@/plugins/katex';
import store from '@/store';
import '@/styles/index.less';
import { GOOGLE_ANALYTICS_ID } from '@/utils/constants';
import filters from '@/utils/filters.js';

import Element from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import Cancel from './components/btn/Cancel.vue';
import IconBtn from './components/btn/IconBtn.vue';
import Save from './components/btn/Save.vue';

import Panel from '@oj/components/Panel.vue';
import VerticalMenuItem from '@oj/components/verticalMenu/verticalMenu-item.vue';
import VerticalMenu from '@oj/components/verticalMenu/verticalMenu.vue';
import 'babel-polyfill';
import 'echarts/lib/chart/bar';
import 'echarts/lib/chart/line';
import 'echarts/lib/chart/pie';
import 'echarts/lib/component/dataZoom';
import 'echarts/lib/component/grid';
import 'echarts/lib/component/legend';
import 'echarts/lib/component/markPoint';
import 'echarts/lib/component/title';
import 'echarts/lib/component/toolbox';
import 'echarts/lib/component/tooltip';

import iView from 'iview';
import 'iview/dist/styles/iview.css';
import Vue from 'vue';
import VueAnalytics from 'vue-analytics';
import VueClipboard from 'vue-clipboard2';

import ECharts from 'vue-echarts/components/ECharts.vue';
import App from './App.vue';
import router from './router';

import VueMeta from 'vue-meta';
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

import vgl from 'vue-golden-layout';

// register global utility filters.
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key]);
});

Vue.config.productionTip = false;
Vue.use(iView, {
  i18n: (key, value) => i18n.t(key, value),
});
Vue.use(Element, {
  i18n: (key, value) => i18n.t(key, value),
});

Vue.use(vgl);
Vue.use(BootstrapVue);
Vue.use(VueMeta);
Vue.use(VueClipboard);
Vue.use(highlight);
Vue.use(katex);
Vue.use(VueAnalytics, {
  id: GOOGLE_ANALYTICS_ID,
  router,
});

Vue.component('ECharts', ECharts);
Vue.component(VerticalMenu.name, VerticalMenu);
Vue.component(VerticalMenuItem.name, VerticalMenuItem);
Vue.component(Panel.name, Panel);

Vue.component(IconBtn.name, IconBtn);
Vue.component(Save.name, Save);
Vue.component(Cancel.name, Cancel);

// ????????????????????????
Vue.prototype.$Message.config({
  duration: 2,
});
Vue.prototype.$error = (s) => Vue.prototype.$Message.error(s);
Vue.prototype.$info = (s) => Vue.prototype.$Message.info(s);
Vue.prototype.$success = (s) => Vue.prototype.$Message.success(s);

new Vue(Vue.util.extend({ router, store, i18n }, App)).$mount('#app');
