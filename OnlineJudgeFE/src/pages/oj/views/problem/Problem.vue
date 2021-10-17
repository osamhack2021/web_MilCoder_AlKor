<template>
<div>
  <Multipane class="vertical-resizer" layout="vertical" @paneResize="verticalPaneResize">
    <div class="pane pane-left" style="width: 50%">
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
      <div class="toolbar-container">
        <div class="toolbar" @click="handleToolbarClick">
          <div>
            <Icon type="arrow-left-b"></Icon>
          </div>
          <div>WORKSPACE/SUBMIT</div>
          <div>
            <Icon type="arrow-left-b"></Icon>
          </div>
        </div>
      </div>
    </div>
    <MultipaneResizer/>
    <div class="pane pane-right" style="flex-grow: 1; width: 200px" ref="paneRight">
      <!--problem main end-->
      <Multipane class="horizontal-resizer" layout="horizontal">
        <div class="pane" style="height: 70%">
          <Card :padding="20" id="submit-code" dis-hover>
            <CodeEditor :source.sync="code"
                        :languages="problem.languages"
                        :language="language"/>
            <Row type="flex" justify="space-between">
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
                  <Alert type="success" show-icon>{{ $t('m.You_have_solved_the_problem') }}</Alert>
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
                <Button type="warning" icon="edit" :loading="submitting" @click="submitCode"
                        :disabled="problemSubmitDisabled || submitted"
                        class="fl-right">
                  <span v-if="submitting">{{ $t('m.Submitting') }}</span>
                  <span v-else>{{ $t('m.Submit') }}</span>
                </Button>
              </Col>
            </Row>
          </Card>
        </div>
        <MultipaneResizer/>
        <div class="pane" style="flex-grow: 1">
          <h1>asdf</h1>
          <h1>asdf</h1>
          <h1>asdf</h1>
        </div>
      </Multipane>
    </div>
  </Multipane>
  <PostEditor :visible="showEditPostDialog" :problemID="problemID" @closeDialog="onCloseEditDialog"></PostEditor>
</div>
</template>

<script>
import { buildProblemCodeKey, CONTEST_STATUS, JUDGE_STATUS } from '@/utils/constants';
import storage from '@/utils/storage';
import api from '@oj/api';
import CodeEditor, { constants } from '@oj/components/CodeEditor';
import PostEditor from '@oj/components/PostEditor';
import { FormMixin } from '@oj/components/mixins';
import { Multipane, MultipaneResizer } from 'vue-multipane';
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
      code: '',
      language: constants.DEFAULT_LANGUAGE_CODE,
      theme: constants.DEFAULT_THEME,
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
        vm.language = problemCode.language;
        vm.code = problemCode.code;
        vm.theme = problemCode.theme;
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

        if (this.code !== '') {
          return;
        }
        // try to load problem template
        this.language = this.problem.languages[0];
        let template = this.problem.template;
        if (template && template[this.language]) {
          this.code = template[this.language];
        }
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
      const toolbar = event.currentTarget;
      const pane = toolbar.parentElement.parentElement;
      const resizer = pane.nextElementSibling;
      const oppositePane = resizer.nextElementSibling;
      const isRight = toolbar.classList.contains('right');

      toolbar.classList = 'toolbar';
      oppositePane.classList.remove('hide');
      pane.style.width = '50%';
      resizer.style.display = null;
      if (isRight) {
        oppositePane.style.width = '200px';
      } else {
        oppositePane.style.height = '200px';
      }
    },
    verticalPaneResize(pane, resizer, size) {
      const rightEl = this.$refs.paneRight;
      const width = rightEl.offsetWidth;
      if (width < 200) {
        const toolbar = pane.querySelector('.toolbar');
        pane.style.width = '100%';
        rightEl.classList.add('hide');
        resizer.style.display = 'none';
        toolbar.classList.add('active');
        toolbar.classList.add('right');
      }
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
      if (this.code.trim() === '') {
        this.$error(this.$i18n.t('m.Code_can_not_be_empty'));
        return;
      }
      this.submissionId = '';
      this.result = { result: 9 };
      this.submitting = true;
      let data = {
        problem_id: this.problem.id,
        language: this.language,
        code: this.code,
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
    onCopy(event) {
      this.$success('Code copied');
    },
    onCopyError(e) {
      this.$error('Failed to copy code');
    },
    onCloseEditDialog() {
      this.showEditPostDialog = false;
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
  },
};
</script>
<style>
.content-app {
  padding: 0 !important;
}
</style>
<style lang="less" scoped>
.toolbar-container {
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

    &.right {
      right: 0;
    }

    &.left {
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
    width: 3px;
    height: 40px;
    position: absolute;
    top: 50%;
    left: 50%;
    margin-top: -20px;
    margin-left: -1.5px;
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
    margin: 0;
    left: 0;
    position: relative;
    border-top: 1px solid #ccc;
    border-bottom: 1px solid #ccc;

    &:before {
      display: block;
      content: "";
      width: 40px;
      height: 3px;
      position: absolute;
      top: 50%;
      left: 50%;
      margin-top: -6.5px;
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

.pane {
  &.hide {
    display: none;
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

#submit-code {
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

.fl-right {
  float: right;
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

