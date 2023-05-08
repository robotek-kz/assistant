<template>
  <div id="main-layout">
    <FileExplorer />
    <Editor />
  </div>
</template>


<script>
import Editor from "@/components/Editor/Editor.vue";
import FileExplorer from "@/components/Editor/FileExplorer.vue";
import { mapGetters, mapActions } from "vuex"
import UnderDevelopment from '@/components/UnderDevelopment.vue';

export default {
  name: 'CodeEditor',
  components: {
    UnderDevelopment,
    FileExplorer,
    Editor
  },
  computed: {
    ...mapGetters("user", ["currentUser"]),
  },

  methods: {
    ...mapActions("files", ["loadFiles"]),
  },
  async mounted() {
    this.loadFiles(this.currentUser.id);
  },
};

</script>


<style scoped>
  #main-layout {
    height: 100%;
    display: grid;
    overflow: hidden;
    grid-template-columns: 300px 1fr;
    background: #F2F4F4;
  }
  </style>
