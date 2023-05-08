<template>
  <div class="file-explorer">
    <header>
      <h4></h4>
      <div class="menu">
        <div class="icon-wrapper">
          <FolderPlusIcon size="18" class="icon" @click="createNewFile" />
          <span class="tooltip">Создать файл</span>
        </div>
        <div class="icon-wrapper">
          <FilePlusIcon size="18" class="icon" @click="createNewFolder" />
          <span class="tooltip">Создать папку</span>
        </div>
    </div>
    </header>
    <simplebar class="content-area">
      <DirectoryListing :files="getChildren('root')" :activeFiles="getActiveFileList  " />
    </simplebar>
  </div>
</template>

<script>
import { FilePlusIcon, FolderPlusIcon } from "vue-feather-icons";
import { mapGetters, mapActions } from "vuex";
import DirectoryListing from "@/components/Editor/DirectoryListing.vue";

export default {
  components: {
    FilePlusIcon,
    FolderPlusIcon,
    DirectoryListing
  },
  computed: {
    ...mapGetters('files', ['getFiles']),
    ...mapGetters('editor', ['getActiveFiles', 'getActiveFileList', 'getChildren']),
    activeFiles() {
      return Object.keys(this.getActiveFiles).reduce((result, editor) => {
        if (this.getActiveFiles[editor]) {
          return Object.assign(result, {
            [this.getActiveFiles[editor].file_id]: true,
          });
        } else {
          return result;
        }
      }, {});
    },
  },
  methods: {
    ...mapActions('files', ['createFile','createFolder']),
    createNewFile() {
      this.createFile({parent: '0', editable: true});
    },
    createNewFolder() {
      this.createFolder({parent: '0', editable: true});
    },
  },
};
</script>

<style scoped>
.file-explorer {
    background: #F3F3F3;
    z-index: 9;
    border-right:2px solid #E30712;
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
    min-width: 0;
    min-height: 0;
}
.file-explorer header {
    display: flex;
    flex-direction: row;
    padding: 5px 10px 5px 10px;
    align-items: center;
    z-index: 99;
}
.file-explorer header h4 {
      color: #212121;
      font-weight: bold;
      flex: 1;
}
.file-explorer header .menu {
  display: flex;
}
.file-explorer header .menu .icon-wrapper {
  position: relative;
}
.file-explorer header .menu .icon-wrapper .tooltip {
  position: absolute;
  background: ghostwhite;
  top: 35px;
  left: -100px;
  white-space: nowrap;
  display: none;
  padding: 5px 10px;
  border-radius: 5px;
}
.file-explorer header .menu .icon-wrapper:hover .tooltip {
  display: flex;
}
.file-explorer header .icon {
    color: black;
    padding: 7px;
    border-radius: 3px;
    transitioN: 0.3s all ease-in-out;
}
.file-explorer header .icon:hover {
    cursor: pointer;
    background: ghostwhite;
    color:  #E30712;
}
.file-explorer header .icon:active {
    opacity: 0.7;
    transform: scale(0.98);
}
.file-explorer .content-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: auto;
}
</style>
