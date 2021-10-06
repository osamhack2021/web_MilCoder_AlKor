<template>
<div id="ide-main" style="height: 600px">
    <!--
    <script type="text/javascript" src="third_party/download.js"></script>
    -->

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
                <button id="run-btn" class="ui primary labeled icon button"><i class="play icon"></i>Run (F9)</button>
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
                            <MonacoEditor class="editor" v-model="code.stdin" language="plaintext" :options=monacoOption> </MonacoEditor>
                        </gl-component>
                    </gl-stack>
                    <gl-stack>
                        <gl-component componentName="stdout" title="실행 결과(STDOUT)">
                            <MonacoEditor class="editor" v-model="code.stdout" language="plaintext" :options=monacoOption> </MonacoEditor>
                        </gl-component>
                        <gl-component componentName="stderr" title="오류(STDERR)">
                            <MonacoEditor class="editor" v-model="code.stderr" language="plaintext" :options=monacoOption> </MonacoEditor>
                        </gl-component>
                        <gl-component componentName="compile output" title="컴파일 결과">
                            <MonacoEditor class="editor" v-model="code.compileOutput" language="plaintext" :options=monacoOption> </MonacoEditor>
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

const supportedLangs = [
  { value: '45', mode: 'UNKNOWN', name: 'Assembly (NASM 2.14.02)' },
  { value: '46', mode: 'shell', name: 'Bash (5.0.0)' },
  { value: '47', mode: 'UNKNOWN', name: 'Basic (FBC 1.07.1)' },
  { value: '1011', mode: 'UNKNOWN', name: 'Bosque (latest)' },
  { value: '75', mode: 'c', name: 'C (Clang 7.0.1)' },
  { value: '1013', mode: 'c', name: 'C (Clang 9.0.1)' },
  { value: '1001', mode: 'c', name: 'C (Clang 10.0.1)' },
  { value: '48', mode: 'c', name: 'C (GCC 7.4.0)' },
  { value: '49', mode: 'c', name: 'C (GCC 8.3.0)' },
  { value: '50', mode: 'c', name: 'C (GCC 9.2.0)' },
  { value: '51', mode: 'csharp', name: 'C# (Mono 6.6.0.161)' },
  { value: '1022', mode: 'csharp', name: 'C# (Mono 6.10.0.104)' },
  { value: '1021', mode: 'csharp', name: 'C# (.NET Core SDK 3.1.302)' },
  { value: '76', mode: 'cpp', name: 'C++ (Clang 7.0.1)' },
  { value: '1014', mode: 'cpp', name: 'C++ (Clang 9.0.1)' },
  { value: '1002', mode: 'cpp', name: 'C++ (Clang 10.0.1)' },
  { value: '52', mode: 'cpp', name: 'C++ (GCC 7.4.0)' },
  { value: '53', mode: 'cpp', name: 'C++ (GCC 8.3.0)' },
  { value: '54', mode: 'cpp', name: 'C++ (GCC 9.2.0)' },
  { value: '1003', mode: 'c', name: 'C3 (latest)' },
  { value: '86', mode: 'clojure', name: 'Clojure (1.10.1)' },
  { value: '77', mode: 'UNKNOWN', name: 'COBOL (GnuCOBOL 2.2)' },
  { value: '55', mode: 'UNKNOWN', name: 'Common Lisp (SBCL 2.0.0)' },
  { value: '56', mode: 'UNKNOWN', name: 'D (DMD 2.089.1)' },
  { value: '57', mode: 'UNKNOWN', name: 'Elixir (1.9.4)' },
  { value: '58', mode: 'UNKNOWN', name: 'Erlang (OTP 22.2)' },
  { value: '44', mode: 'plaintext', name: 'Executable' },
  { value: '87', mode: 'fsharp', name: 'F# (.NET Core SDK 3.1.202)' },
  { value: '1024', mode: 'fsharp', name: 'F# (.NET Core SDK 3.1.302)' },
  { value: '59', mode: 'UNKNOWN', name: 'Fortran (GFortran 9.2.0)' },
  { value: '60', mode: 'go', name: 'Go (1.13.5)' },
  { value: '88', mode: 'UNKNOWN', name: 'Groovy (3.0.3)' },
  { value: '61', mode: 'UNKNOWN', name: 'Haskell (GHC 8.8.1)' },
  { value: '62', mode: 'java', name: 'Java (OpenJDK 13.0.1)' },
  { value: '1004', mode: 'java', name: 'Java (OpenJDK 14.0.1)' },
  { value: '63', mode: 'javascript', name: 'JavaScript (Node.js 12.14.0)' },
  { value: '78', mode: 'kotlin', name: 'Kotlin (1.3.70)' },
  { value: '64', mode: 'lua', name: 'Lua (5.3.5)' },
  { value: '1009', mode: 'python', name: 'Nim (stable)' },
  { value: '79', mode: 'objective-c', name: 'Objective-C (Clang 7.0.1)' },
  { value: '65', mode: 'UNKNOWN', name: 'OCaml (4.09.0)' },
  { value: '66', mode: 'UNKNOWN', name: 'Octave (5.1.0)' },
  { value: '67', mode: 'pascal', name: 'Pascal (FPC 3.0.4)' },
  { value: '85', mode: 'perl', name: 'Perl (5.28.1)' },
  { value: '68', mode: 'php', name: 'PHP (7.4.1)' },
  { value: '43', mode: 'plaintext', name: 'Plain Text' },
  { value: '69', mode: 'UNKNOWN', name: 'Prolog (GNU Prolog 1.4.5)' },
  { value: '70', mode: 'python', name: 'Python (2.7.17)' },
  { value: '71', mode: 'python', name: 'Python (3.8.1)' },
  { value: '1010', mode: 'python', name: 'Python for ML (3.7.3)' },
  { value: '80', mode: 'r', name: 'R (4.0.0)' },
  { value: '72', mode: 'ruby', name: 'Ruby (2.7.0)' },
  { value: '73', mode: 'rust', name: 'Rust (1.40.0)' },
  { value: '81', mode: 'UNKNOWN', name: 'Scala (2.13.2)' },
  { value: '83', mode: 'swift', name: 'Swift (5.2.3)' },
  { value: '74', mode: 'typescript', name: 'TypeScript (3.7.4)' },
  { value: '84', mode: 'vb', name: 'Visual Basic.Net (vbnc 0.0.0.5943)' },
];

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
        source: 'hello',
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
});
</script>


<style scoped>
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

#ide-main {
    width: 100%;
    height: 100%;
    min-height: 600px;
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