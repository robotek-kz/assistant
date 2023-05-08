<template>
    <codemirror
    ref="cmEditor"
    :value="code"
    :options="cmOptions"
    :autoCloseTags="true"
    @ready="onCmReady"
    @focus="onCmFocus"
    @input="onCmCodeChange"
  />
</template>


<script>
import { codemirror } from "vue-codemirror";
import "codemirror/lib/codemirror.css";
import "codemirror/mode/javascript/javascript.js";
import "codemirror/mode/gfm/gfm"
import "codemirror/mode/markdown/markdown"
import "codemirror/mode/python/python.js";
import "codemirror/theme/eclipse.css";
import "codemirror/theme/base16-light.css"
import "codemirror/addon/edit/closebrackets"
import "codemirror/addon/edit/closetag"
export default {
    components: {
      codemirror
    },
    props: {
        file: Object
    },
    data() {
    return {
      code: '',
      cmOptions: {
        // codemirror options
        tabSize: 4,
        mode: "python",
        theme: "eclipse",
        lineNumbers: true,
        line: true,
        foldGutter: true,
        highlightFormatting: true,
        xml: true,
        autoCloseBrackets: true,
        autoCloseTags: true
        // more codemirror options, 更多 codemirror 的高级配置...
      },
    };
  },
  methods: {
    onCmReady(cm) {
      console.log("the editor is readied!", cm);
    },
    onCmFocus(cm) {
      console.log("the editor is focused!", cm);
    },
    onCmCodeChange(newCode) {
      console.log("this is new code", newCode);
      this.code = newCode;
      this.$emit('contentChanged', newCode);;
    },
  },
  computed: {
    codemirror() {
      return this.$refs.cmEditor.codemirror;
    },
  },
  watch: {
    file(newFile) {
      console.log('from watch:', newFile);
      this.code = newFile.content || '';
    }
  },
  created() {
    this.code = this.file? this.file.content: ''
  }
}

</script>


<style>
.vue-codemirror {
	 min-height: 100%;
   width: 100%;
}
 .vue-codemirror .CodeMirror {
	 height: 100%;
	 font-family: "Fira Code", monospace;
	 font-size: 16px !important;
}
 .vue-codemirror .CodeMirror .CodeMirror-overlayscroll-vertical div, .vue-codemirror .CodeMirror .CodeMirror-overlayscroll-horizontal div {
	 background-color: rgba(24, 65, 147, 0.45)!important;
}
 .vue-codemirror .CodeMirror pre {
	 word-break: break-word;
}
 .vue-codemirror .CodeMirror-gutters {
	 background-color: transparent !important;
}
</style>