<template>
  <div style="margin: 0 0 15px 0">
    <Row type="flex" justify="space-between" class="header">
      <Col :span=12>
        <div class="tools">
          <span>{{ $t('m.Language') }}:</span>
          <Select :value="editor.language" @on-change="onLanguageChange" class="adjust">
            <Option v-for="item in supportLanguages" :key="item.id" :value="item.lang">
              {{ item.name }}
            </Option>
          </Select>
          <div>
            <Tooltip :content="this.$i18n.t('m.Editor_run')" class="editor-menu" placement="top">
              <Button icon="play"></Button>
            </Tooltip>
            <Tooltip :content="this.$i18n.t('m.Upload_file')" class="editor-menu" placement="top">
              <Button icon="upload" @click="onUploadFile"/>
            </Tooltip>
            <Tooltip :content="this.$i18n.t('m.Reset_to_default_code_definition')" class="editor-menu" placement="top">
              <Button icon="refresh" @click="onResetClick"/>
            </Tooltip>
          </div>
          <input type="file" id="file-uploader" style="display: none" @change="onUploadFileDone">
        </div>
      </Col>
      <Col :span=12>
        <div class="fl-right">
          <span>{{ $t('m.Theme') }}:</span>
          <Select :value="editor.theme" @on-change="onThemeChange" class="adjust">
            <Option v-for="item in themes" :key="item" :value="item">{{ item.toUpperCase() }}
            </Option>
          </Select>
        </div>
      </Col>
    </Row>
    <Row type="flex">
      <Col :span=24>
        <MonacoEditor
          ref="source"
          class="editor"
          :options="options"
          :language="editor.language"
          :value="editor.source"
          :theme="editor.theme"
        />
      </Col>
    </Row>
  </div>
</template>

<script>
import axios from 'axios';
import MonacoEditor from 'vue-monaco';
import {
  DEFAULT_LANGUAGE,
  DEFAULT_LANGUAGE_CODE,
  DEFAULT_THEME,
  LANGUAGES_BY_CODE,
  LANGUAGES_BY_LANG,
  THEMES,
} from './constants';

// TODO: 코드 테스트용 API(@oj/api) 생성 후 제거
const JUDGE_URL = 'https://ce.judge0.com';

export default {
  name: 'CodeEditor',
  components: {
    MonacoEditor,
  },
  props: {
    source: {
      type: String,
      default: '',
    },
    languages: {
      type: Array,
      default: [],
    },
    language: {
      type: String,
      default: DEFAULT_LANGUAGE,
    },
    theme: {
      type: String,
      default: DEFAULT_THEME,
    },
  },
  data() {
    const code = this.language || DEFAULT_LANGUAGE_CODE;
    const language = LANGUAGES_BY_CODE[code].lang;
    return {
      options: {
        automaticLayout: true,
        scrollBeyondLastLine: true,
        minimap: {
          enabled: false,
        },
      },
      editor: {
        language,
        theme: this.theme,
        source: this.source || LANGUAGES_BY_LANG[language].template,
      },
      supportLanguages: [],
      themes: THEMES,
    };
  },
  methods: {
    run() {
      const data = {
        language_id: LANGUAGES_BY_CODE[this.editor.language].id,
        source_code: this.editor.source,
        stdin: this.editor.stdin,
        compiler_options: '',
        command_line_arguments: '',
        redirect_stderr_to_stdout: false,
      };

      axios({
        url: `${JUDGE_URL}/submissions`,
        method: 'POST',
        data: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: false,
      })
        .then((res) => res.json())
        .then((res) => {
          console.log(res);
        });
    },
    onLanguageChange(newLang) {
      this.editor = Object.assign({}, this.editor, {
        language: newLang,
        source: LANGUAGES_BY_LANG[newLang].template,
      });
    },
    onThemeChange(newTheme) {
      this.editor = Object.assign({}, this.editor, {
        theme: newTheme,
      });
    },
    onResetClick() {
      this.editor = Object.assign({}, this.editor, {
        source: LANGUAGES_BY_LANG[this.editor.language].template,
      });
      this.$nextTick(() => {
        this.monacoEditor.getModel().setValue(this.editor.source);
      });
    },
    onUploadFile() {
      document.getElementById('file-uploader').click();
    },
    onUploadFileDone() {
      const self = this;
      const fileReader = new window.FileReader();
      const fileUploadEl = document.getElementById('file-uploader');
      const f = fileUploadEl.files[0];
      fileReader.onload = (e) => {
        self.monacoEditor.getModel().setValue(e.target.result);
        fileUploadEl.value = '';
      };
      fileReader.readAsText(f, 'UTF-8');
    },
  },
  computed: {
    monacoEditor() {
      return this.$refs.source.getEditor();
    },
  },
  watch: {
    'languages'(languages) {
      this.supportLanguages = languages.map((code) => LANGUAGES_BY_CODE[code]).filter(Boolean);
    },
  },
};
</script>
<style lang="less" scoped>
.header {
  margin: 5px 5px 15px 5px;
  min-width: 480px;

  .tools {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    margin-top: -10px;

    & > * {
      flex: 0 1 auto;
      justify-content: flex-start;
      margin: 10px 10px 0 0;
    }
  }

  .adjust {
    width: 150px;
  }

  .fl-right {
    float: right;
  }
}

.editor-menu {
  margin-left: 10px;
}
</style>

<style>
.editor {
  width: 100%;
  height: 100%;
  min-height: 300px;
  margin: 0;
  padding: 0;
}
</style>
