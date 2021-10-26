<template>
  <MonacoEditor
    ref="code"
    class="editor"
    :value.sync="value"
    :options="options"
    :language="language"
    theme="vs"
  />
</template>

<script>
import MonacoEditor from 'vue-monaco';
import { DEFAULT_LANGUAGE } from './constants';

export default {
  name: 'CodeEditor',
  components: {
    MonacoEditor,
  },
  props: {
    value: {
      type: String,
      default: '',
    },
    languages: {
      type: Array,
      default: () => [],
    },
    language: {
      type: String,
      default: DEFAULT_LANGUAGE,
    },
    onStdinChange: Function,
  },
  data() {
    return {
      options: {
        automaticLayout: true,
        scrollBeyondLastLine: true,
        minimap: {
          enabled: false,
        },
      },
    };
  },
  methods: {
    getEditor() {
      return this.$refs.code.getEditor();
    },
    getModel() {
      return this.getEditor().getModel();
    },
    layout() {
      this.getEditor().layout();
    },
    get() {
      try {
        return this.getModel().getValue();
      } catch (e) {
        return undefined;
      }
    },
    set(value) {
      return this.getModel().setValue(value);
    },
  },
};
</script>
<style scoped>
.editor {
  width: 100%;
  height: 100%;
  min-height: 300px;
  margin: 0;
  padding: 0;
}
</style>
