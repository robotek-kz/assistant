<template>

</template>

<script>
import UnderDevelopment from '@/components/UnderDevelopment.vue';
import CodeDiffViewer from '@/components/Diff/CodeDiffViewer.vue';
import SideBar from '@/components/SideBar.vue';
import Window from '@/components/GameSketch/Window.vue';


export default {
  name: 'Rating',
  components: {
    UnderDevelopment,
    CodeDiffViewer,
    SideBar,
    Window,
  },
  data() {
    return {
      oldStr: '',
      newStr: ''
    };
  },
  created() {
    // this.$store.dispatch('resetModuleState');
    this.oldStr = '[\n    {\n        name: tit\n        displaySurname: "标题"\n        datatype: "OBJECT"\n    }\n]';
    this.newStr =  '[\n    {\n        name: title\n        displayName: "标题"\n        datatype: "OBJECT"\n    }\n    {\n        name: tit\n        displaySurname: "标题"\n        datatype: "OBJECT"\n    }\n\n    {\n        name: tit\n        displaySurname: "标题"\n        datatype: "OBJECT"\n    }\n\n    {\n        name: tit\n        displaySurname: "标题"\n        datatype: "OBJECT"\n    }\n\n    {\n        name: tit\n        displaySurname: "标题"\n        datatype: "OBJECT"\n    }\n\n    {\n        name: tit\n        displaySurname: "标题"\n        datatype: "OBJECT"\n    }\n]';
  }
};
</script>

<style scoped>
main {
  height: 100%;
  width: 100%;
}

</style>
