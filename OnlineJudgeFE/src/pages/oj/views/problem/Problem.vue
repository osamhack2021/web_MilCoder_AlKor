<template>
<div>
  <Multipane class="vertical-resizer" layout="vertical" @paneResize="verticalPaneResize">
    <div
      class="pane pane-left"
      :class="{ full: toolbar.variant === 'v-right', hide: toolbar.variant === 'v-left' }"
      ref="paneLeft">
      <div id="problem-main">
        <!--problem main-->
        <Panel :padding="40" shadow style="height: 100%">
          <div slot="title">{{ problem.title }}</div>
          <Button slot="extra" type="info" icon="ios-open-outline" @click.native="showEditPostDialog = true">
            {{ $t('m.NewPost') }}
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
            <Row type="flex" justify="space-between" style="height: 100%;">
              <Col :span="24">
                <CodeEditor
                  ref="editor"
                  :value.sync="workspace.code"
                  :language="workspace.language"
                  :languages="problem.languages"
                  :submission="submission"
                  :onLanguageChange="onLanguageChange"
                  :onThemeChange="onThemeChange"
                />
              </Col>
              <Col :span="10">
                <div class="status" v-if="statusVisible">
                  <template v-if="!this.contestID || (this.contestID && OIContestRealTimePermission)">
                    <span>{{ $t('m.Status') }}</span>
                    <Tag type="dot" :color="submissionStatus.color" @click.native="handleRoute('/status/'+submissionId)">
                      {{ $t('m.' + submissionStatus.text.replace(/ /g, '_')) }}
                    </Tag>
                  </template>
                  <template v-else-if="this.contestID && !OIContestRealTimePermission">
                    <Alert type="success" show-icon>{{ $t('m.Submitted_successfully') }}</Alert>
                  </template>
                </div>
                <div v-else-if="problem.my_status === 0">
                  <Alert type="success" show-icon>{{
                      $t('m.You_have_solved_the_problem')
                    }}
                  </Alert>
                </div>
                <div v-else-if="this.contestID && !OIContestRealTimePermission && submissionExists">
                  <Alert type="success" show-icon>{{
                      $t('m.You_have_submitted_a_solution')
                    }}
                  </Alert>
                </div>
                <div v-if="contestEnded">
                  <Alert type="warning" show-icon>{{ $t('m.Contest_has_ended') }}</Alert>
                </div>
              </Col>
              <Col :span="12">
                <template v-if="captchaRequired">
                  <div class="captcha-container">
                    <Tooltip v-if="captchaRequired" content="Click to refresh" placement="top">
                      <img :src="captchaSrc" @click="getCaptchaSrc"/>
                    </Tooltip>
                    <Input v-model="captchaCode" class="captcha-code"/>
                  </div>
                </template>
              </Col>
            </Row>
          </Card>
        </div>
        <MultipaneResizer/>
        <div class="pane pane-bottom" ref="paneBottom">
          <Card :padding="10" id="workspace-io">
            <Tabs :animated="false" @on-click="handleIoTabClick">
              <TabPane label="INPUT" name="stdin">
                <CodeEditor
                  :value.sync="workspace.stdin"
                  :options="workspace.options"
                  :theme="workspace.theme"
                  language="plaintext"
                  ref="stdinEditor"
                />
              </TabPane>
              <TabPane label="OUTPUT" name="stdout">
                <CodeEditor
                  :value.sync="workspace.stdout"
                  :options="Object.assign({}, workspace.options, { readOnly: true })"
                  :theme="workspace.theme"
                  language="plaintext"
                  ref="stdoutEditor"
                />
              </TabPane>
              <TabPane label="ERROR" name="stderr">
                <CodeEditor
                  :value.sync="workspace.stderr"
                  :options="Object.assign({}, workspace.options, { readOnly: true })"
                  :theme="workspace.theme"
                  language="plaintext"
                  ref="stderrEditor"
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
import { buildProblemCodeKey, CONTEST_STATUS, JUDGE_STATUS, SUBMITTING } from '@/utils/constants';
import storage from '@/utils/storage';
import api from '@oj/api';
import CodeEditor from '@oj/components/CodeEditor';
import {
  DEFAULT_LANGUAGE,
  DEFAULT_THEME,
  LANGUAGE_TO_ALIAS,
  LANGUAGES_BY_ALIAS,
  LANGUAGES_BY_LANG,
} from '@oj/components/CodeEditor/constants';
import PostEditor from '@oj/components/PostEditor';
import { FormMixin } from '@oj/components/mixins';
import { Multipane, MultipaneResizer } from '@oj/components/Multipane';
import { assign } from 'lodash';
import { mapActions, mapGetters } from 'vuex';
import { types } from '../../../../store';
import { largePie, pie } from './chartData';

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
      paneSize: 0,
      statusVisible: false,
      captchaRequired: false,
      graphVisible: false,
      submissionExists: false,
      captchaCode: '',
      captchaSrc: '',
      contestID: '',
      problemID: '',
      submitting: false,
      submissionId: '',
      submitted: false,
      result: {
        result: 9,
      },
      problem: {
        title: '',
        description: '',
        hint: '',
        my_status: '',
        template: {},
        languages: [],
        created_by: {
          username: '',
        },
        tags: [],
        io_mode: { 'io_mode': 'Standard IO' },
      },
      submission: {
        handler: this.submitCode,
        status: '',
        disabled: false,
      },
      workspace: {
        code: LANGUAGES_BY_LANG[DEFAULT_LANGUAGE].template,
        language: DEFAULT_LANGUAGE,
        theme: DEFAULT_THEME,
        stdin: '',
        stdout: '',
        stderr: '',
        options: {
          automaticLayout: true,
          scrollBeyondLastLine: true,
          minimap: {
            enabled: false,
          },
        },
        currentTab: 'stdin',
      },
      toolbar: {
        label: '',
        variant: '', // v-left, v-right, h-top, h-bottom
      },
      pie: pie,
      largePie: largePie,

      largePieInitOpts: {
        width: '500',
        height: '480',
      },
    };
  },
  beforeRouteEnter(to, from, next) {
    let problemCode = storage.get(buildProblemCodeKey(to.params.problemID, to.params.contestID));
    if (problemCode) {
      next(vm => {
        vm.workspace = assign({}, vm.workspace, {
          code: problemCode.code,
          language: problemCode.language,
          theme: problemCode.theme,
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
          this.submissionExists = res.data.data;
        });
        problem.languages = problem.languages.sort();
        this.problem = problem;
        this.changePie(problem);

        // try to load problem template
        const language = LANGUAGES_BY_ALIAS[this.problem.languages[0]];
        this.workspace = assign({}, this.workspace, {
          code: language.template,
          language: language.lang,
          theme: DEFAULT_THEME,
          stdin: problem.samples.map((sample) => sample.input).join(''),
        });
      }, () => {
        this.$Loading.error();
      });
    },
    changePie(problemData) {
      for (let k in problemData.statistic_info) {
        if (filtedStatus.indexOf(k) === -1) {
          delete problemData.statistic_info[k];
        }
      }
      let acNum = problemData.accepted_number;
      let data = [
        { name: 'WA', value: problemData.submission_number - acNum },
        { name: 'AC', value: acNum },
      ];
      this.pie.series[0].data = data;
      let data2 = JSON.parse(JSON.stringify(data));
      data2[1].selected = true;
      this.largePie.series[1].data = data2;

      let legend = Object.keys(problemData.statistic_info).map(ele => JUDGE_STATUS[ele].short);
      if (legend.length === 0) {
        legend.push('AC', 'WA');
      }
      this.largePie.legend.data = legend;

      let acCount = problemData.statistic_info['0'];
      delete problemData.statistic_info['0'];

      let largePieData = [];
      Object.keys(problemData.statistic_info).forEach(ele => {
        largePieData.push({
          name: JUDGE_STATUS[ele].short,
          value: problemData.statistic_info[ele],
        });
      });
      largePieData.push({ name: 'AC', value: acCount });
      this.largePie.series[0].data = largePieData;
    },
    handleRoute(route) {
      this.$router.push(route);
    },
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
    verticalPaneResize(pane, resizer, size) {
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
      this.$nextTick(() => {
        this.layoutEditors();
      });
    },
    handleIoTabClick(name) {
      const editor = this.$refs[`${name}Editor`];
      this.currentTab = name;
      this.$nextTick(() => {
        editor.monacoEditor.layout();
      });
    },
    checkSubmissionStatus() {
      if (this.refreshStatus) {
        clearTimeout(this.refreshStatus);
      }
      const checkStatus = () => {
        let id = this.submissionId;
        api.getSubmission(id).then(res => {
          this.result = res.data.data;
          if (Object.keys(res.data.data.statistic_info).length !== 0) {
            this.submitting = false;
            this.submitted = false;
            clearTimeout(this.refreshStatus);
            this.init();
          } else {
            this.refreshStatus = setTimeout(checkStatus, 2000);
          }
        }, res => {
          this.submitting = false;
          clearTimeout(this.refreshStatus);
        });
      };
      this.refreshStatus = setTimeout(checkStatus, 2000);
    },
    submitCode() {
      const code = this.editor.getModel().getValue();
      if (code.trim() === '') {
        this.$error(this.$i18n.t('m.Code_can_not_be_empty'));
        return;
      }

      this.submissionId = '';
      this.result = { result: SUBMITTING };
      this.submitting = true;
      const data = {
        problem_id: this.problem.id,
        language: LANGUAGE_TO_ALIAS[this.workspace.language],
        code: code,
        contest_id: this.contestID,
      };
      if (this.captchaRequired) {
        data.captcha = this.captchaCode;
      }
      const submitFunc = (data, detailsVisible) => {
        this.statusVisible = true;
        api.submitCode(data).then(res => {
          this.submissionId = res.data.data && res.data.data.submission_id;
          // 定时检查状态
          this.submitting = false;
          this.submissionExists = true;
          if (!detailsVisible) {
            this.$Modal.success({
              title: this.$i18n.t('m.Success'),
              content: this.$i18n.t('m.Submit_code_successfully'),
            });
            return;
          }
          this.submitted = true;
          this.checkSubmissionStatus();
        }, res => {
          this.getCaptchaSrc();
          if (res.data.data.startsWith('Captcha is required')) {
            this.captchaRequired = true;
          }
          this.submitting = false;
          this.statusVisible = false;
        });
      };

      if (this.contestRuleType === 'OI' && !this.OIContestRealTimePermission) {
        if (this.submissionExists) {
          this.$Modal.confirm({
            title: '',
            content: '<h3>' + this.$i18n.t('m.You_have_submission_in_this_problem_sure_to_cover_it') + '<h3>',
            onOk: () => {
              setTimeout(() => {
                submitFunc(data, false);
              }, 1000);
            },
            onCancel: () => {
              this.submitting = false;
            },
          });
        } else {
          submitFunc(data, false);
        }
      } else {
        submitFunc(data, true);
      }
    },
    layoutEditors() {
      this.$refs.editor.monacoEditor.layout();
      this.$refs[`${this.workspace.currentTab}Editor`].monacoEditor.layout();
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
    onLanguageChange(newLang) {
      this.workspace = assign({}, this.workspace, {
        language: newLang,
        code: LANGUAGES_BY_LANG[newLang].template,
      });
    },
    onThemeChange(newTheme) {
      this.workspace = assign({}, this.workspace, { theme: newTheme });
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
      return {
        text: JUDGE_STATUS[this.result.result]['name'],
        color: JUDGE_STATUS[this.result.result]['color'],
      };
    },
    submissionRoute() {
      if (this.contestID) {
        return { name: 'contest-submission-list', query: { problemID: this.problemID } };
      } else {
        return { name: 'submission-list', query: { problemID: this.problemID } };
      }
    },
    editor() {
      return this.$refs.editor.monacoEditor;
    },
  },
  beforeRouteLeave(to, from, next) {
    clearInterval(this.refreshStatus);

    this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, { menu: true });
    storage.set(buildProblemCodeKey(this.problem._id, from.params.contestID), {
      code: this.code,
      language: this.language,
      theme: this.theme,
    });
    next();
  },
  watch: {
    '$route'() {
      this.init();
    },
    submitting() {
      this.submission = assign({}, this.submission, {
        status: this.submitting ? SUBMITTING : this.submission.status,
      });
    },
    problemSubmitDisabled() {
      this.submission = assign({}, this.submission, {
        disabled: this.problemSubmitDisabled || this.submitted,
      });
    },
    submitted() {
      this.submission = assign({}, this.submission, {
        disabled: this.problemSubmitDisabled || this.submitted,
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
  height: calc(100vh - 4em);
  margin-top: 20px;
}

.vertical-resizer > .pane {
  text-align: left;
  overflow: hidden;
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
  height: 100%;

  .status {
    float: left;

    span {
      margin-right: 10px;
      margin-left: 10px;
    }
  }

  .captcha-container {
    display: inline-block;

    .captcha-code {
      width: auto;
      margin-top: -20px;
      margin-left: 20px;
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

