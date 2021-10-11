<template>
<div id="ide-main" style="height: 600px">
    <div id="ide-navigation" class="ui small inverted menu">
        <div id="ide-header" class="header item">
            <img id="site-icon" src="/static/images/mil-icon.png">
            <h2 id="ide-title" class="wide screen only">MilCoder Soure Editor</h2>
        </div>
        <div class="left menu">
            <div class="ui dropdown item site-links on-hover wide screen only"> 코드 초기화 <i class="new icon"></i>
            </div>
            <div class="item borderless">
                <select v-model="selectedLang" id="select-language" class="ui dropdown">
                    <option v-for="lang in supportedLangs" :value=lang.value :mode=lang.mode :key=lang.value>{{lang.name}}</option>
                </select>
            </div>
            <div class="item no-left-padding borderless">
                <button id="run-btn" class="ui primary labeled icon button" v-on:click="run()"><i class="play icon"></i>Run (F9)</button>
            </div>
            <div id="navigation-message" class="item borderless">
                <span class="navigation-message-text"></span>
            </div>
        </div>
    </div>

    <div id="ide-content">
        <golden-layout id="ide-layout" reorderEnabled="false">
            <gl-col>
                <gl-component componentName="source" title="소스코드">
                    <MonacoEditor class="editor" v-model="code.source" language="cpp" :options=monacoOption> </MonacoEditor>
                </gl-component>
                <gl-row>
                    <gl-stack>
                        <gl-component componentName="stdin" title="입력(STDIN)">
                            <MonacoEditor id="monaco-stdin" class="editor" v-model="code.stdin" language="plaintext" :options=monacoOption> </MonacoEditor>
                        </gl-component>
                    </gl-stack>
                    <gl-stack>
                        <gl-component componentName="stdout" title="실행 결과(STDOUT)">
                            <MonacoEditor id="monaco-stdout" class="editor" v-model="code.stdout" language="plaintext" :options=monacoOption> </MonacoEditor>
                        </gl-component>
                        <gl-component componentName="stderr" title="오류(STDERR)">
                            <MonacoEditor id="monaco-stderr" class="editor" v-model="code.stderr" language="plaintext" :options=monacoOption> </MonacoEditor>
                        </gl-component>
                        <gl-component componentName="compile output" title="컴파일 결과">
                            <MonacoEditor id="monaco-compileOutput" class="editor" v-model="code.compileOutput" language="plaintext" :options=monacoOption> </MonacoEditor>
                        </gl-component>
                    </gl-stack>
                </gl-row>
            </gl-col>
        </golden-layout>
    </div>

    <div id="site-modal" class="ui modal">
        <div class="header">
            <i class="close icon"></i>
            <span id="title"></span>
        </div>
        <div class="scrolling content"></div>
        <div class="actions">
            <div class="ui small labeled icon cancel button">
                <i class="remove icon"></i>
                Close (ESC)
            </div>
        </div>
    </div>

    <div id="site-footer">
        <div id="editor-status-line"></div>
        <span id="status-line"></span>
    </div>
</div>
</template>

<script>
import $ from 'jquery';
import MonacoEditor from 'vue-monaco';

function updateResize() {
  $('#ide-layout').width($('#ide-content').width());
  $('#ide-layout').height($('#ide-content').height());
  var display = window.innerWidth <= 800 ? 'none' : '';
  $('.wide.screen.only').each(function (index) {
    $(this).css('display', display);
  });
}

export default ({
  setup() {},

  mounted() {
    updateResize();

    $(window).resize(function () {
      updateResize();
    });
  },

  data() {
    return {
      monacoOption: {
        theme: 'vs-dark',
        automaticLayout: true,
        scrollBeyondLastLine: true,
        minimap: {
          enabled: false
        }
      },
      supportedLangs: supportedLangs,
      selectedLang: '54',
      code: {
        source: cppSource,
        stdin: '',
        stdout: '',
        stderr: '',
        compileOutput: ''
      }
    };
  },

  components: {
    MonacoEditor,
  },

  watch: {
    selectedLang: function(newVal, oldVal){
      for(var lang of supportedLangs){
        if(lang.value == this.selectedLang){
          this.code.source = lang.template;
          break
        }
      }
    }
  },

  metaInfo: {
    meta: [{ charset: 'utf-8' }],
    link: [
      {
        rel: 'stylesheet',
        href: 'https://cdnjs.cloudflare.com/ajax/libs/golden-layout/1.5.9/css/goldenlayout-base.css',
        integrity: 'sha256-oIDR18yKFZtfjCJfDsJYpTBv1S9QmxYopeqw2dO96xM=',
        crossorigin: 'anonymous',
      },
      {
        rel: 'stylesheet',
        href: 'https://cdnjs.cloudflare.com/ajax/libs/golden-layout/1.5.9/css/goldenlayout-dark-theme.css',
        integrity: 'sha256-ygw8PvSDJJUGLf6Q9KIQsYR3mOmiQNlDaxMLDOx9xL0=',
        crossorigin: 'anonymous',
      },
      {
        rel: 'stylesheet',
        href: 'https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css',
        integrity: 'sha256-9mbkOfVho3ZPXfM7W8sV2SndrGDuh7wuyLjtsWeTI1Q=',
        crossorigin: 'anonymous',
      },
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css?family=Exo+2',
      },
    ],
    script: [
      {
        src: 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js',
        integrity: 'sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=',
        crossorigin: 'anonymous'
      },
      {
        src: 'https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js',
        integrity: 'sha256-t8GepnyPmw9t+foMh3mKNvcorqNHamSKtKRxxpUEgFI=',
        crossorigin: 'anonymous'
      }
    ]
  },

  methods: {
    run() {
      $('#run-btn').addClass("loading");

      this.code.stdout = 'loading...';
      this.code.stderr = 'loading...';
      this.code.compileOutput = 'loading...';

      var sourceValue = this.code.source;
      var stdinValue = this.code.stdin;
      var languageId = this.selectedLang;

      var data = {
          source_code: sourceValue,
          language_id: languageId,
          stdin: stdinValue,
          compiler_options: '',
          command_line_arguments: '',
          redirect_stderr_to_stdout: false
      };

      $.ajax({
          url: judgeURL + `/submissions`,
          type: "POST",
          async: true,
          contentType: "application/json",
          data: JSON.stringify(data),
          xhrFields: {
              withCredentials: judgeURL.indexOf("/secure") != -1 ? true : false
          },
          success: function (data, textStatus, jqXHR) {
              console.log(`Your submission token is: ${data.token}`);
              setTimeout(function(){this.fetchSubmission(data.token)}.bind(this), check_timeout);
          }.bind(this)
      });
    },
    handleResult(data) {
      console.log('handle result');
      console.log(data);
      $('#run-btn').removeClass("loading");

      var time = (data.time === null ? "-" : data.time + "s");
      var memory = (data.memory === null ? "-" : data.memory + "KB");
      var status = data.status || '';
      var stdout = data.stdout|| '';
      var stderr = data.stderr|| '';
      var compile_output = data.compile_output || '';
      
      stdout += '\n\nFinished in '+time+', with '+memory+' memory.';

      this.code.stdout = stdout;
      this.code.stderr = stderr;
      this.code.compileOutput = compile_output;
    },
    fetchSubmission(submission_token) {
      console.log('fetch submission');
      console.log(submission_token);
      $.ajax({
          url: judgeURL + "/submissions/" + submission_token,
          type: "GET",
          async: true,
          success: function (data, textStatus, jqXHR) {
              console.log(data);
              if (data.status.id <= 2) { // In Queue or Processing
                  setTimeout(function(){this.fetchSubmission(submission_token)}.bind(this), check_timeout);
                  return;
              }
              this.handleResult.bind(this, data)();
          }.bind(this)
        });
    }
  }
});

var check_timeout = 300;
var judgeURL = "https://ce.judge0.com";

// Template Sources
var cSource = "\
#include <stdio.h>\n\
\n\
int main(void) {\n\
    printf(\"Hello Judge0!\\n\");\n\
    return 0;\n\
}\n\
";

var cppSource = "\
#include <iostream>\n\
\n\
int main() {\n\
    std::cout << \"hello, world\" << std::endl;\n\
    return 0;\n\
}\n\
";

var javaSource = "\
public class Main {\n\
    public static void main(String[] args) {\n\
        System.out.println(\"hello, world\");\n\
    }\n\
}\n\
";

var javaScriptSource = "console.log(\"hello, world\");";

var pythonSource = "print(\"hello, world\")";

var supportedLangs = [
  { value: '50', mode: 'c', name: 'C (GCC 9.2.0)', template: cSource },
  { value: '54', mode: 'cpp', name: 'C++ (GCC 9.2.0)', template: cppSource},
  { value: '62', mode: 'java', name: 'Java (OpenJDK 13.0.1)', template: javaSource },
  { value: '63', mode: 'javascript', name: 'JavaScript (Node.js 12.14.0)', template: javaScriptSource },
  { value: '70', mode: 'python', name: 'Python (2.7.17)', template: pythonSource },
  { value: '71', mode: 'python', name: 'Python (3.8.1)', template: pythonSource },
];

</script>


<style scoped>
#ide-main {
    width: 100%;
    height: 100%;
    min-height: 600px;
}

#ide-navigation {
    border-radius: 0;
    margin: 0;
    background: #1e1e1e;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    height: 45px;
}

#ide-header {
    padding-left: 0;
    padding-top: 0;
    padding-bottom: 0;
}

#ide-title {
    margin: 0;
    display: inline;
    vertical-align: middle;
    font-family: 'Exo 2', sans-serif;
}

#ide-content {
    width: 100%;
    height: 100%;
}

#ide-settings {
    height: 300px;
    width: 600px;
    position: relative;
}

.editor {
    width: 100%;
    height: 100%;
}
</style>