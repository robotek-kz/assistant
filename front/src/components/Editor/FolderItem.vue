<template>
    <div class="folder-wrapper">
      <div :class="['file-item', {active: isActive}]">
        <div class="clickable-area" @click="toggleShowChildren" @dbclick="readonly = !readonly">
          <FolderMinusIcon v-if="showChildren" class="icon" size="18" />
          <FolderIcon v-else class="icon" size="18" />
          <form @submit.prevent="$refs.input.blur()">

            <input 
              :ref="'input'"
              type="text"
              v-model="filename"
              :readonly="readonly"
              size="2"
              @blur="changeFileName"
            />

          </form>
        </div>
        <div class="context-menu">
          <MoreVerticalIcon
            class="trigger-icon no-margin"
            size="18"
            @click="toggleContextMenu"
          />
          <SlideYUpTransition>
            <div 
              v-if="showContextMenu"
              class="options"
              v-click-outside="toggleContextMenu"
            >
              <div class="option-item" @click="createNewFile">
                <file-plus-icon size="18" class="icon" />Создать файл
              </div>
              <div class="option-item" @click="createNewFolder">
                <folder-plus-icon size="18" class="icon" />Создать папку
              </div>
              <div class="option-item" @click="openRenameMode">
                <edit3-icon size="18" class="icon" />Переименовать
              </div>
              <div class="option-item" @click="deleteCurrentFolder">
                <trash2-icon size="18" class="icon" />Удалить папку
              </div>
            </div>
          </SlideYUpTransition>
        </div>
      </div>
      <div v-if="showChildren" class="files">
        <component
          v-for="child in getChildren(file.file_id)"
          :key="child.id"
          :is="child.type"
          :file="child"
          :isActive="!!getActiveFileList[child.id]"
        />
      </div>
    </div>
</template>
  
<script>
import {
  FolderIcon,
  FolderPlusIcon,
  FilePlusIcon,
  MoreVerticalIcon,
  Trash2Icon,
  Edit3Icon,
  DownloadIcon,
  CopyIcon,
  ClipboardIcon,
  FolderMinusIcon
} from "vue-feather-icons";
import { mapActions, mapGetters} from "vuex";
import { SlideYUpTransition, FadeTransition } from "vue2-transitions";
import FileItem from "@/components/Editor/FileItem";
import FolderItem from "@/components/Editor/FolderItem";
import { fileTypes } from "@/models/vFile.model"; 
export default {
    name: "folder",
    components: {
      FolderIcon,
      MoreVerticalIcon,
      Trash2Icon,
      Edit3Icon,
      DownloadIcon,
      CopyIcon,
      ClipboardIcon,
      SlideYUpTransition,
      FolderPlusIcon,
      FolderMinusIcon,
      FilePlusIcon,
      [fileTypes.FILE]: FileItem,
      [fileTypes.FOLDER]: FolderItem,
      FadeTransition,
    },
    props: {
      file: Object,
      isActive: Boolean,
    },
    data() {
      return {
        readonly: true,
        filename: "",
        showContextMenu: false,
        showChildren: false,
      };
    },
    computed: {
      ...mapGetters("editor", ["getChildren", "getActiveFileList"]),
      children() {
        const cs = this.getChildren(this.file.file_id);
        return cs;
      },
    },
    methods: {
      ...mapActions("files",[
        "renameFile",
        "deleteFolder",
        "createFile",
        "createFolder",
      ]),
      changeFileName() {
        if (this.filename) {
          this.renameFile({file_id: this.file.file_id, name: this.filename});
          this.readonly = true;
        } else {
          this.deleteFile({file_id: this.file.file_id})
        }
      },
      openRenameMode() {
        this.showContextMenu = false;
        this.readonly = false;
        this.$refs.input.focus();
      },
      toggleContextMenu() {
        this.showContextMenu = !this.showContextMenu;
      },
      deleteCurrentFolder() {
        this.showContextMenu = !this.showContextMenu;
        this.deleteFolder({ folder_id: this.file.file_id });
      },
      createNewFile() {
        this.showChildren = true;
        this.createFile({ parent: this.file.file_id, editable: true });
        this.showContextMenu = false;
      },
      createNewFolder() {
        this.createFolder({ parent: this.file.file_id, editable: true });
        this.showContextMenu = false;
      },
      toggleShowChildren() {
        this.showChildren = !this.showChildren;
        console.log('showChildren', this.showChildren)
      },
    },
    watch: {
      readonly(value) {
        if (!value) {
          this.$refs.input.focus();
        }
      },
    },
    mounted() {
      this.readonly = !this.file.editable;
      this.filename = this.file.name;
      if (this.file.editable) {
        this.$refs.input.focus();
      }
    },
    created() {
      this.fileTypes = fileTypes;
    }
  };
</script>
  
<style scoped>
.folder-wrapper {
  display: flex;
  flex-direction: column;
}
.folder-wrapper .files {
  margin-left: 10px;
  display: flex;
  flex-direction: column;
}

.file-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 2px 5px 2px 0;
  margin: 2px 5px;
  border-radius: 5px;
}

.file-item.active {
  background: #FFCDD2;
}

.file-item .clickable-area {
  display: flex;
  align-items: center;
  flex: 1;
  padding: 3px 10px;
}

.file-item .icon {
  margin-right: 10px;
  width: 20px;
}

.file-item form {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.file-item input {
  border: 0;
  padding: 6px 8px;
  border-radius: 2px;
  color: #212121;
  border: 2px solid transparent;
  outline: none;
  transition: 0.2s all ease-in-out;
  background: transparent;
  min-width: 0;
}

.file-item input[readonly] {
  pointer-events: none;
}

.file-item input:focus {
  border-bottom: 2px solid #E30712;
}

.file-item .context-menu {
    display: none;
    align-items: center;
    justify-content: center;
    align-items: center;
    position: relative;
    transition: 0.3s all ease-in-out;
}

.file-item .context-menu .trigger-icon {
  visibility: hidden;
  padding: 5px;
  border-radius: 5px;
  margin-right: 5px;
}


.file-item .context-menu .trigger-icon.no-margin {
  margin-right: 0;
}

.file-item .context-menu .trigger-icon:hover {
  background: #E30712;
}

.file-item .context-menu .trigger-icon:active {
  transform: scale(0.95);
}

.file-item .context-menu .options {
  position: absolute;
  right: 0;
  top: 35px;
  width: 170px;
  height: auto;
  z-index: 99;
  display: flex;
  flex-direction: column;
  border-radius: 5px;
  background: ghostwhite;
  box-shadow: #212121;
  border: 1px solid #212121;
  padding: 5px;
}

.file-item .context-menu .options .option-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-radius: 3px;
}

.file-item .context-menu .options .option-item:hover {
  cursor: pointer;
  color: #212121;
}

.file-item:hover {
  background: ghostwhite;
    cursor: pointer;
  /* color: whitesmoke; */
}

.file-item:hover .context-menu {
  display: flex;
}

.file-item:hover .context-menu .trigger-icon {
  visibility: visible;
}

</style>