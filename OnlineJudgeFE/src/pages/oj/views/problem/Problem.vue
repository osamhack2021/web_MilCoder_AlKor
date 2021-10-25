<template>
  <div>
    <Multipane class="vertical-resizer" layout="vertical" @paneResize="handlePaneResize">
      <div
        class="pane pane-left"
        :class="{ full: toolbar.variant === 'v-right', hide: toolbar.variant === 'v-left' }"
        ref="paneLeft">
        <div id="problem-main">
          <!--problem main-->
          <Panel :padding="40" shadow style="height: 100%">
            <div slot="title">{{ problem.title }}</div>
            <Button
              @click.native="showEditPostDialog = true"
              slot="extra" type="info" icon="edit">
              새 질문
            </Button>
            <Button
              @click.native="$router.push('/qna/'+problemID)"
              slot="extra" type="success" icon="android-open">
              질문 보기
            </Button>
            <div id="problem-content" class="markdown-body" v-katex>
              <p class="title">{{ $t('m.Description') }}</p>
              <p class="content" v-html=problem.description></p>
              <!-- {{$t('m.music')}} -->
              <p class="title">{{ $t('m.Input') }}
                <span v-if="problem.io_mode.io_mode=='File IO'">({{ $t('m.FromFile') }}: {{
                    problem.io_mode.input
                  }})</span></p>
              <p class="content" v-html=problem.input_description></p>

              <p class="title">{{ $t('m.Output') }}
                <span v-if="problem.io_mode.io_mode=='File IO'">({{ $t('m.ToFile') }}: {{
                    problem.io_mode.output
                  }})</span></p>
              <p class="content" v-html=problem.output_description></p>

              <div v-for="(sample, index) of problem.samples" :key="index">
                <div class="flex-container sample">
                  <div class="sample-input">
                    <p class="title">{{ $t('m.Sample_Input') }} {{ index + 1 }}
                      <a class="copy"
                         v-clipboard:copy="sample.input"
                         v-clipboard:success="onCopy"
                         v-clipboard:error="onCopyError">
                        <Icon type="clipboard"></Icon>
                      </a>
                    </p>
                    <pre>{{ sample.input }}</pre>
                  </div>
                  <div class="sample-output">
                    <p class="title">{{ $t('m.Sample_Output') }} {{ index + 1 }}</p>
                    <pre>{{ sample.output }}</pre>
                  </div>
                </div>
              </div>
              <div v-if="problem.hint">
                <p class="title">{{ $t('m.Hint') }}</p>
                <Card dis-hover>
                  <div class="content" v-html=problem.hint></div>
                </Card>
              </div>
              <div v-if="problem.source">
                <p class="title">{{ $t('m.Source') }}</p>
                <p class="content">{{ problem.source }}</p>
              </div>
            </div>
          </Panel>
        </div>
      </div>
      <MultipaneResizer :class="{ hide: toolbar.variant.startsWith('v-') }"/>
      <div
        class="pane pane-right"
        :class="{ full: toolbar.variant === 'v-left', hide: toolbar.variant === 'v-right' }"
        ref="paneRight">
        <!--problem main end-->
        <Multipane class="horizontal-resizer" layout="horizontal" ref="horizontalMultipane">
          <div class="pane pane-top" ref="paneTop">
            <Card :padding="10" id="workspace-code" dis-hover>
              <div class="header">
                <div class="tools">
                  <div class="languages">
                    <span>{{ $t('m.Language') }}:</span>
                    <Select :value="workspace.language" @on-change="handleLanguageChange">
                      <Option v-for="item in workspace.languages" :key="item.id" :value="item.lang">
                        {{ item.name }}
                      </Option>
                    </Select>
                  </div>
                  <Tooltip :content="this.$i18n.t('m.Editor_run')" class="editor-menu" placement="bottom">
                    <Button type="primary" icon="play" @click="runCode"></Button>
                  </Tooltip>
                  <Tooltip :content="this.$i18n.t('m.Upload_file')" class="editor-menu" placement="bottom">
                    <Button type="primary" icon="upload" @click="handleUploadFile"/>
                  </Tooltip>
                  <Tooltip :content="this.$i18n.t('m.Reset_to_default_code_definition')" class="editor-menu" placement="bottom">
                    <Button type="warning" icon="refresh" @click="handleResetClick"/>
                  </Tooltip>
                  <Tooltip :content="this.$i18n.t('m.Submit')" class="editor-menu" placement="bottom">
                    <Button
                      :loading="submission.state === SUBMISSION_STATES.SUBMITTING"
                      :disabled="submission.disabled"
                      @click="submitCode"
                      type="error" icon="paper-airplane">
                      <span v-if="submission.state === SUBMISSION_STATES.SUBMITTING">
                        {{ $t('m.Submitting') }}
                      </span>
                      <span v-else>{{ $t('m.Submit') }}</span>
                    </Button>
                  </Tooltip>
                  <input type="file" id="file-uploader" style="display: none" @change="handleUploadFileDone">
                </div>
                <div class="status" v-if="submission.sentOnce && submission.id">
                  <template v-if="!this.contestID || (this.contestID && OIContestRealTimePermission)">
                    <span>{{ $t('m.Status') }}</span>
                    <Tag type="dot" :color="submissionStatus.color" @click.native="handleRoute('/status/' + submission.id)">
                      {{ $t('m.' + submissionStatus.text.replace(/ /g, '_')) }}
                    </Tag>
                  </template>
                  <template v-else-if="this.contestID && !OIContestRealTimePermission">
                    <Alert type="success" show-icon>{{ $t('m.Submitted_successfully') }}</Alert>
                  </template>
                  <template v-else-if="problem.my_status === SUBMISSION_STATES.ACCEPTED">
                    <Alert type="success" show-icon>{{
                        $t('m.You_have_solved_the_problem')
                      }}
                    </Alert>
                  </template>
                  <template v-else-if="this.contestID && !OIContestRealTimePermission && submissionExists">
                    <Alert type="success" show-icon>{{
                        $t('m.You_have_submitted_a_solution')
                      }}
                    </Alert>
                  </template>
                  <template v-if="contestEnded">
                    <Alert type="warning" show-icon>{{ $t('m.Contest_has_ended') }}</Alert>
                  </template>
                </div>
              </div>
              <div>
                <CodeEditor
                  ref="editor"
                  :value.sync="workspace.code"
                  :language="workspace.language"
                  :languages="problem.languages"
                  :submission="submission"
                  :onLanguageChange="handleLanguageChange"
                />
              </div>
            </Card>
          </div>
          <MultipaneResizer/>
          <div class="pane pane-bottom" ref="paneBottom">
            <Card :padding="10" id="workspace-io">
              <Tabs :value="workspace.tab" :animated="false" @on-click="handleWorkspaceTabClick">
                <TabPane label="INPUT" name="stdin">
                  <CodeEditor
                    :value.sync="workspace.io.stdin"
                    :options="workspace.options"
                    :onStdinChange="onStdinChange"
                    language="plaintext"
                    ref="stdinEditor"
                  />
                </TabPane>
                <TabPane label="OUTPUT" name="stdout">
                  <CodeEditor
                    :value.sync="workspace.io.stdout"
                    :options="Object.assign({}, workspace.options, { readOnly: true })"
                    language="plaintext"
                    ref="stdoutEditor"
                  />
                </TabPane>
                <TabPane label="ERROR" name="stderr">
                  <CodeEditor
                    :value.sync="workspace.io.stderr"
                    :options="Object.assign({}, workspace.options, { readOnly: true })"
                    language="plaintext"
                    ref="stderrEditor"
                  />
                </TabPane>
                <TabPane label="COMPILATION" name="compile">
                  <CodeEditor
                    :value.sync="workspace.result.compile"
                    :options="Object.assign({}, workspace.options, { readOnly: true })"
                    language="plaintext"
                    ref="compileEditor"
                  />
                </TabPane>
              </Tabs>
            </Card>
          </div>
        </Multipane>
      </div>
      <div class="toolbar-container" @click="handleToolbarClick">
        <div class="toolbar" :class="{ active: !!toolbar.variant, [toolbar.variant]: !!toolbar.variant }">
          <div>
            <Icon v-if="toolbar.variant === 'v-right'" type="arrow-left-b"></Icon>
            <Icon v-else-if="toolbar.variant === 'v-left'" type="arrow-right-b"></Icon>
          </div>
          <div>{{ toolbar.label }}</div>
          <div>
            <Icon v-if="toolbar.variant === 'v-right'" type="arrow-left-b"></Icon>
            <Icon v-else-if="toolbar.variant === 'v-left'" type="arrow-right-b"></Icon>
          </div>
        </div>
      </div>
    </Multipane>
    <PostEditor :visible="showEditPostDialog" :problemID="problemID" @closeDialog="onCloseEditDialog"></PostEditor>
  </div>
</template>

<script>
import {
  ACCEPTED,
  buildProblemCodeKey,
  CONTEST_STATUS,
  JUDGE_STATUS,
  SUBMITTING,
} from '@/utils/constants';
import storage from '@/utils/storage';
import api from '@oj/api';
import CodeEditor from '@oj/components/CodeEditor';
import {
  DEFAULT_LANGUAGE,
  LANGUAGE_TO_ALIAS,
  LANGUAGES_BY_ALIAS,
  LANGUAGES_BY_LANG,
} from '@oj/components/CodeEditor/constants';
import { FormMixin } from '@oj/components/mixins';
import { Multipane, MultipaneResizer } from '@oj/components/Multipane';
import PostEditor from '@oj/components/PostEditor';
import axios from 'axios';
import { assign, isEmpty } from 'lodash';
import { mapActions, mapGetters } from 'vuex';
import { types } from '../../../../store';

const JUDGE_URL = `${location.protocol}//${location.hostname}:2358`;
const JUDGE_CHECK_INTERVAL = 500;
const filtedStatus = ['-1', '-2', '0', '1', '2', '3', '4', '8'];

export default {
  name: 'Problem',
  components: {
    CodeEditor,
    PostEditor,
    Multipane,
    MultipaneResizer,
  },
  mixins: [FormMixin],
  data() {
    return {
      showEditPostDialog: false,
      submissionExists: false,
      contestID: '',
      problemID: '',
      problem: {
        title: '',
        description: '',
        hint: '',
        my_status: '',
        template: {},
        languages: [],
        created_by: { username: '' },
        tags: [],
        io_mode: { 'io_mode': 'Standard IO' },
      },
      SUBMISSION_STATES: { ACCEPTED, SUBMITTING },
      submission: {
        id: undefined,
        state: undefined,
        handler: this.submitCode,
        sentOnce: false,
        disabled: false,
      },
      workspace: {
        code: LANGUAGES_BY_LANG[DEFAULT_LANGUAGE].template,
        language: DEFAULT_LANGUAGE,
        languages: [],
        io: {
          stdin: '',
          stdout: '',
          stderr: '',
        },
        result: {
          compile: '',
          memory: '',
          time: '',
        },
        options: {
          automaticLayout: true,
          scrollBeyondLastLine: true,
          minimap: {
            enabled: false,
          },
        },
        tab: 'stdin',
      },
      toolbar: {
        label: '',
        variant: '', // v-left, v-right, h-top, h-bottom
      },
    };
  },
  beforeRouteEnter(to, from, next) {
    const problemCode = storage.get(buildProblemCodeKey(to.params.problemID, to.params.contestID));
    if (problemCode) {
      next(vm => {
        vm.workspace = assign({}, vm.workspace, {
          code: problemCode.code,
          language: problemCode.language,
        });
      });
    } else {
      next();
    }
  },
  mounted() {
    this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, { menu: false });
    this.init();
  },
  methods: {
    ...mapActions(['changeDomTitle']),
    init() {
      this.$Loading.start();
      this.contestID = this.$route.params.contestID;
      this.problemID = this.$route.params.problemID;
      let func = this.$route.name === 'problem-details' ? 'getProblem' : 'getContestProblem';
      api[func](this.problemID, this.contestID).then(res => {
        this.$Loading.finish();
        let problem = res.data.data;
        this.changeDomTitle({ title: problem.title });
        api.submissionExists(problem.id).then(res => {
          this.submission = assign({}, this.submission, {
            sentOnce: res.data.data,
            state: problem['my_status'],
          });
        });
        problem.languages = problem.languages.sort();
        this.problem = problem;
        // this.changePie(problem);

        const language = this.workspace.language || LANGUAGES_BY_ALIAS[this.problem.languages[0]];
        const languages = (
          this.workspace.languages.length
            ? this.workspace.languages
            : problem.languages.map((alias) => LANGUAGES_BY_ALIAS[alias]).filter(Boolean)
        );
        const code = this.mainEditor.get() || language.template;
        this.workspace = assign({}, this.workspace, {
          code,
          language,
          languages,
        });
      }, () => {
        this.$Loading.error();
      });
    },
    handleRoute(route) {
      this.$router.push(route);
    },
    checkSubmissionStatus() {
      const tick = setInterval(() => {
        api.getSubmission(this.submission.id).then((res) => {
          const { data } = res.data;
          this.submission = assign({}, this.submission, {
            state: data.result,
          });
          if (!isEmpty(data['statistic_info'])) {
            clearInterval(tick);
            this.init();
          }
        });
      }, 2000);
    },
    runCode() {
      const self = this;
      const code = this.mainEditor.get();
      const stdin = this.stdinEditor.get();
      const data = {
        language_id: LANGUAGES_BY_LANG[this.workspace.language].id,
        source_code: btoa(code),
        stdin: btoa(stdin),
        compiler_options: '',
        command_line_arguments: '',
        redirect_stderr_to_stdout: false,
      };
      const submit = () => axios({
        url: `${JUDGE_URL}/submissions?base64_encoded=true`,
        method: 'POST',
        data: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' },
        withCredentials: false,
      });
      const check = (token) => axios({
        url: `${JUDGE_URL}/submissions/${token}?base64_encoded=true`,
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        withCredentials: false,
      });
      this.onRunStart();
      submit(data).then((res) => {
        const token = res.data.token;
        const t = setInterval(() => {
          check(token).then((res) => {
            const data = res.data;
            if (data.status.id <= 2) {
              return;
            }
            const stdout = [
              data.stdout ? atob(data.stdout) : '',
              `Finished in ${data.time}s with ${data.memory} bytes memory usage.`,
            ].join('\n');
            self.workspace = Object.assign({}, self.workspace, {
              io: {
                stdin,
                stdout,
                stderr: data.stderr ? atob(data.stderr) : null,
              },
              result: {
                time: data.time,
                memory: data.memory,
                compile: data['compile_output']
                  ? decodeURIComponent(
                    atob(data['compile_output'])
                      .split('')
                      .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
                      .join(''))
                  : null,
              },
            });
            self.$nextTick(() => {
              self.onRunEnd();
            });
            clearInterval(t);
          });
        }, JUDGE_CHECK_INTERVAL);
      });
    },
    submitCode() {
      const code = this.mainEditor.get();
      if (code.trim() === '') {
        this.$error(this.$i18n.t('m.Code_can_not_be_empty'));
        return;
      }

      const data = {
        code,
        language: LANGUAGE_TO_ALIAS[this.workspace.language],
        problem_id: this.problem.id,
        contest_id: this.contestID,
      };
      const submissionCheck = ((
        this.contestRuleType === 'OI' &&
        !this.OIContestRealTimePermission &&
        this.submission.sentOnce)
        ? new Promise((resolve, reject) => {
          this.$Modal.confirm({
            title: '',
            content: `<h3>${this.$i18n.t('m.You_have_submission_in_this_problem_sure_to_cover_it')}</h3>`,
            onOk: () => resolve(),
            onCancel: () => {
              this.submission = assign({}, this.submission, { state: undefined });
              reject();
            },
          });
        })
        : Promise.resolve());

      submissionCheck
        .then(() => api.submitCode(data))
        .then((res) => {
          const { data } = res.data;
          this.submission = assign({}, this.submission, {
            id: data['submission_id'],
            state: SUBMITTING,
            sentOnce: true,
          });
          this.$Modal.success({
            title: this.$i18n.t('m.Success'),
            content: this.$i18n.t('m.Submit_code_successfully'),
          });
          setTimeout(this.checkSubmissionStatus, 1000);
        })
        .catch(() => {
          this.$Modal.error({
            title: this.$i18n.t('m.Cancel'),
            content: this.$i18n.t('m.Submission_canceled'),
          });
        });

    },
    layoutEditors() {
      this.mainEditor.layout();
      this.$refs[`${this.workspace.tab}Editor`].layout();
    },
    // Handle DOM events
    handleToolbarClick(event) {
      const container = event.currentTarget;
      const pane = container.parentElement.firstElementChild;
      const resizer = pane.nextElementSibling;
      const oppositePane = resizer.nextElementSibling;

      switch (this.toolbar.variant) {
        case 'v-left':
        case 'v-right':
          pane.style.width = '50%';
          oppositePane.style.width = '50%';
          oppositePane.style.width = null;
          break;
        case 'v-top':
        case 'v-bottom':
          pane.style.height = '70%';
          oppositePane.style.height = '30%';
          oppositePane.style.height = null;
          break;
      }
      this.toolbar = { label: '', variant: '' };
      this.$nextTick(() => {
        this.layoutEditors();
      });
    },
    handlePaneResize(pane, resizer, size) {
      const oppositePane = resizer.nextElementSibling;
      const hideLeft = pane.offsetWidth < 200;
      const hideRight = oppositePane.offsetWidth < 200;

      if (!hideLeft && !hideRight) return;

      if (hideLeft) {
        this.toolbar = assign({}, this.toolbar, {
          label: 'PROBLEM',
          variant: 'v-left',
        });
      } else if (hideRight) {
        this.toolbar = assign({}, this.toolbar, {
          label: 'WORKSPACE/SUBMIT',
          variant: 'v-right',
        });
      }
    },
    // Handle change in properties
    handleLanguageChange(newLang) {
      this.workspace = assign({}, this.workspace, {
        language: newLang,
        code: LANGUAGES_BY_LANG[newLang].template,
      });
    },
    handleUploadFile() {
      document.getElementById('file-uploader').click();
    },
    handleUploadFileDone() {
      const self = this;
      const fileReader = new window.FileReader();
      const fileUploadEl = document.getElementById('file-uploader');
      const f = fileUploadEl.files[0];
      fileReader.onload = (e) => {
        self.mainEditor.set(e.target.result);
        fileUploadEl.value = '';
      };
      fileReader.readAsText(f, 'UTF-8');
    },
    handleResetClick() {
      const template = LANGUAGES_BY_LANG[this.language].template;
      this.value = template;
      this.mainEditor.set(template);
    },
    handleWorkspaceTabClick(name) {
      const editor = this.$refs[`${name}Editor`];
      this.workspace.tab = name;
      this.$nextTick(() => {
        editor.layout();
      });
    },
    // Handle workspace events
    onRunStart() {
      this.workspace = assign({}, this.workspace, {
        io: {
          ...this.workspace,
          stdout: 'loading...',
          stderr: '',
        },
        result: {
          compile: '',
          memory: '',
          time: '',
        },
        tab: 'stdout',
      });
      this.$nextTick(() => {
        this.$refs.stdoutEditor.layout();
      });
    },
    onRunEnd() {
      let tab = this.workspace.tab;
      const { io, result } = this.workspace;
      if (result.compile !== null) {
        tab = 'compile';
      } else if (io.stderr !== null) {
        tab = 'stderr';
      } else {
        tab = 'stdout';
      }
      this.workspace = assign({}, this.workspace, { tab });
      this.$nextTick(() => {
        this.$refs[`${tab}Editor`].layout();
      });
    },
    onCopy(event) {
      this.$success('Code copied');
    },
    onCopyError(e) {
      this.$error('Failed to copy code');
    },
    onCloseEditDialog() {
      this.showEditPostDialog = false;
    },
    onStdinChange(stdin) {
      this.workspace = assign({}, this.workspace, {
        io: {
          ...this.workspace.io,
          stdin,
        },
      });
    },
  },
  computed: {
    ...mapGetters(['problemSubmitDisabled', 'contestRuleType', 'OIContestRealTimePermission', 'contestStatus']),
    contest() {
      return this.$store.state.contest.contest;
    },
    contestEnded() {
      return this.contestStatus === CONTEST_STATUS.ENDED;
    },
    submissionStatus() {
      const state = this.submission.state || 9;
      return {
        text: JUDGE_STATUS[state]['name'],
        color: JUDGE_STATUS[state]['color'],
      };
    },
    mainEditor() {
      return this.$refs.editor;
    },
    stdinEditor() {
      return this.$refs.stdinEditor;
    },
  },
  beforeRouteLeave(to, from, next) {
    clearInterval(this.refreshStatus);

    this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, { menu: true });
    storage.set(buildProblemCodeKey(this.problem._id, from.params.contestID), {
      code: this.mainEditor.get(),
      language: this.workspace.language,
    });
    next();
  },
  watch: {
    '$route'() {
      this.init();
    },
    problemSubmitDisabled() {
      this.submission = assign({}, this.submission, {
        disabled: this.problemSubmitDisabled,
      });
    },
    toolbar() {
      this.layoutEditors();
      this.$nextTick(() => {
        this.layoutEditors();
      });
    },
  },
};
</script>
<style>
.content-app {
  padding: 0 !important;
}
</style>
<style lang="less" scoped>
.hide {
  display: none;
}

.pane-left {
  width: 50%;

  &.full {
    width: 100% !important;
    padding-right: 40px;
  }
}

.pane-right {
  width: 200px;
  flex-grow: 1;

  &.full {
    width: 100% !important;
    padding-left: 40px;
  }
}

.pane-top {
  height: 70%;
  min-height: 300px;

  &.full {
    height: 100% !important;
    padding-left: 40px;
  }
}

.pane-bottom {
  height: 200px;
  flex-grow: 1;
}

.toolbar-container {
  position: initial !important;
  display: inline-block;

  .toolbar {
    display: none;
    opacity: 0;
    transition: opacity 0.3s ease;
    cursor: pointer;
    align-items: center;
    background-color: #fff;
    width: 40px;
    height: 100%;
    flex-direction: column;
    position: absolute;
    top: 0;
    z-index: 5;
    border-left: 1px solid #ccc;
    border-right: 1px solid #ccc;
    justify-content: space-evenly;

    &.v-right {
      right: 0;
    }

    &.v-left {
      left: 0;
    }

    &.active {
      display: flex;
      opacity: 1;
    }

    > * {
      display: flex;
      align-items: center;
    }

    > :first-child, &:last-child {
      //flex: .5;
      font-size: 1.8rem;
    }

    > :nth-child(2) {
      //flex: 1;
      transform: rotate(90deg);

      > div {
        text-transform: uppercase;
        font-weight: bold;
        font-size: 130%;
        white-space: nowrap;
        margin-top: -.4em;
        transform: translateY(10%);
      }
    }
  }
}

.vertical-resizer {
  width: 100%;
  height: calc(100vh - 80px);
}

.vertical-resizer > .pane {
  text-align: left;
  overflow-x: hidden;
  background: #eee;
}

.vertical-resizer > .multipane-resizer {
  margin: 0;
  left: 0;
  position: relative;
  border-left: 1px solid #ccc;
  border-right: 1px solid #ccc;

  &:before {
    display: block;
    content: "";
    width: 5px;
    height: 40px;
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -20px;
    margin-left: -4.5px;
    border-left: 1px solid #ccc;
    border-right: 1px solid #ccc;
  }

  &:hover {
    &:before {
      border-color: #999;
    }
  }
}

.horizontal-resizer {
  width: 100%;
  height: 100%;

  > .pane {
    overflow: hidden;
    background: #eee;
  }

  > .multipane-resizer {
    background: #fff;
    margin: 0 !important;
    left: 0;
    position: relative;
    border-top: 1px solid #ccc;
    border-bottom: 1px solid #ccc;

    &:before {
      display: block;
      content: "";
      width: 40px;
      height: 5px;
      position: absolute;
      top: 50%;
      left: 50%;
      margin-top: -2.5px;
      margin-left: -20px;
      border-top: 1px solid #ccc;
      border-bottom: 1px solid #ccc;
    }
  }

  &:hover {
    &:before {
      border-color: #999;
    }
  }
}

.card-title {
  margin-left: 8px;
}

#problem-main {
  flex: auto;
  height: 100%;

  > div {
    height: 100%;
    overflow-x: hidden;
  }
}

.flex-container {
  #right-column {
    flex: none;
    width: 220px;
  }
}

#problem-content {
  margin-top: -50px;

  .title {
    font-size: 20px;
    font-weight: 400;
    margin: 25px 0 8px 0;
    color: #3091f2;

    .copy {
      padding-left: 8px;
    }
  }

  p.content {
    margin-left: 25px;
    margin-right: 20px;
    font-size: 15px
  }

  .sample {
    align-items: stretch;

    &-input, &-output {
      width: 50%;
      flex: 1 1 auto;
      display: flex;
      flex-direction: column;
      margin-right: 5%;
    }

    pre {
      flex: 1 1 auto;
      align-self: stretch;
      border-style: solid;
      background: transparent;
    }
  }
}

#workspace-code {
  display: flex;
  flex-direction: column;

  .header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;

    .tools {
      display: flex;
      justify-content: space-evenly;
      align-items: center;
      flex-wrap: nowrap;

      .languages {
        display: inline-flex;
        min-width: 240px;
        align-items: center;

        & > span {
          display: inline-flex;
          flex: 1 0 auto;
          margin-right: 0.8em;
        }
      }

      div:not(:last-child) {
        margin-right: 1em;
      }
    }
  }

  .status {
    span {
      margin-right: 10px;
      margin-left: 10px;
    }
  }
}

#info {
  margin-bottom: 20px;
  margin-top: 20px;

  ul {
    list-style-type: none;

    li {
      border-bottom: 1px dotted #e9eaec;
      margin-bottom: 10px;

      p {
        display: inline-block;
      }

      p:first-child {
        width: 90px;
      }

      p:last-child {
        float: right;
      }
    }
  }
}

#workspace-io {
  height: 100%;
}

#pieChart {
  .echarts {
    height: 250px;
    width: 210px;
  }

  #detail {
    position: absolute;
    right: 10px;
    top: 10px;
  }
}

#pieChart-detail {
  margin-top: 20px;
  width: 500px;
  height: 480px;
}
</style>

