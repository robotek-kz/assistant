<template>
  <div :class="['editor-area', getEditorMode]">
    <div id="primary-editor" class="codemirror-instances">
      <TopBar
        :editor="getEditors.primary"
        :activeFile="getActiveFiles[getEditors.primary]"
        :openFiles="getOpenFiles[getEditors.primary]"
      />
      <div class="scroll-wrapper">
      <CodeMirror
         v-if="getActiveFiles[getEditors.primary]"
         :file="getActiveFiles[getEditors.primary]"
         @contentChanged="
         (contents) =>
            updateContents(getActiveFiles[getEditors.primary].file_id, contents)"
      />
      </div>
    </div>
    <div
       v-if="getEditorMode === 'multiple'"
       id="secondary-editor"
       class="codemirror-instances"
      >
      <TopBar
        :editor="getEditors.secondary"
        :activeFile="getActiveFiles[getEditors.secondary]"
        :openFiles="getOpenFiles[getEditors.secondary]"
      />

      <CodeMirror
         v-if="getActiveFiles[getEditors.secondary]"
         :file="getActiveFiles[getEditors.secondary]"
      />

    </div>
  </div>
</template>

<script>
import CodeMirror from "@/components/Editor/CodeMirror.vue";
import TopBar from "@/components/Editor/TopBar.vue";
import { mapActions, mapGetters } from "vuex";
import { EDITORS } from "@/store/modules/editor/initialState";
import debounce from "lodash/debounce";

export default {
  name: "Editor",
  components: {
    CodeMirror,
    TopBar
  },
  data() {
    return {
      code: `*  Welcome to CodeEditor`,
      cmOptions: {
        // codemirror options
        tabSize: 4,
        mode: "text/javascript",
        theme: "dracula",
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
  computed: {
    ...mapGetters("editor", [
      "getActiveEditor",
      "getOpenFiles",
      "getActiveFiles",
    ]),
    getEditors() {
      return EDITORS;
    },
    getEditorMode() {
      if (
        this.getOpenFiles[EDITORS.secondary] &&
        this.getOpenFiles[EDITORS.secondary] > 0
      ) {
        console.log("MULTIPLE");
        return "multiple";
      } else {
        console.log("SINGLE");
        return "single";
      }
    },
    codemirror() {
      return this.$refs.cmEditor.codemirror;
    },
  },
  methods: {
    ...mapActions("files", ["updateFileContents"]),
    updateContents(file_id, content) {
      this.debouncedFileUpdate({file_id, content});
    },
  },
  created() {
    this.debouncedFileUpdate = debounce(this.updateFileContents, 1000);
  },
};
</script>

<style scoped>
.editor-area {
	 display: grid;
   height: 100%;
   overflow: hidden;
}
.editor-area.single {
	 grid-template-columns: 1fr;
}
.editor-area.multiple {
	 grid-template-columns: 1fr 1fr;
}
 .editor-area .codemirror-instances {
	 flex: 1;
	 display: flex;
   height: 100%;
	 flex-direction: column;
   overflow: hidden;
}

.editor-area .scroll-wrapper {
  height: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: auto;
}
 
</style>
