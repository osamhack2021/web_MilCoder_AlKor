// element UI
import elenUS from 'element-ui/lib/locale/lang/en';
// ivew UI
import ivenUS from 'iview/dist/locale/en-US';
import Vue from 'vue';
import VueI18n from 'vue-i18n';

Vue.use(VueI18n);

const languages = [
  { value: 'ko-KO', label: 'Korean', iv: ivenUS, el: elenUS },
  { value: 'en-US', label: 'English', iv: ivenUS, el: elenUS },
  { value: 'zh-CN', label: '简体中文', iv: ivzhCN, el: elzhCN },
  { value: 'zh-TW', label: '繁體中文', iv: ivzhTW, el: elzhTW },
];
const messages = {};

// combine admin and oj
for (let lang of languages) {
  let locale = lang.value;
  let m = require(`./oj/${locale}`).m;
  Object.assign(m, require(`./admin/${locale}`).m);
  let ui = Object.assign(lang.iv, lang.el);
  messages[locale] = Object.assign({ m: m }, ui);
}
// load language packages
export default new VueI18n({
  locale: 'ko-KO',
  messages: messages,
});

export { languages };
