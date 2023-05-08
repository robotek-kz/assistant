<template>
  <div class="topbar">
    <ul class="file-tabs">
      <li 
          v-for="file in openFiles"
          :key="file.file_id"
          :class="[{ active: file.file_id === (activeFile ? activeFile.file_id : null) }]"
          @click="setActiveFile({editor, file_id: file.file_id})"
      >
          <span>{{ file.name }} </span>
        <XIcon 
          size="16" 
          class="icon" 
          @click.stop="closeFile({editor, file_id: file.file_id})" />
      </li>
    </ul>
  </div>
</template>

<script>
import { XIcon } from "vue-feather-icons";
import { mapActions, mapGetters } from "vuex";
export default {
  components: {
    XIcon,
  },
  props: {
    editor: String,
    openFiles: Array,
    activeFile: Object,
  },
  methods: {
    ...mapActions("editor", ["closeFile", "setActiveFile"]),
  },
};
</script>

<style scoped>
.topbar {
  display: flex;
  flex-direction: row;
  align-items: center;
  overflow: auto;
}
.topbar > .file-tabs {
    list-style-type: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: row;
    align-items: center;
}
.topbar .file-tabs li {
    padding: 7px 5px 7px 15px;
    opacity: 0.7;
    background: white;
    color: black;
    margin-top: 2px;
    display: flex;
    flex-direction: row;
    align-items: center;
    border-radius: 5px 5px 0 0;
    border-bottom: 2px solid white;
    max-width: 150px;
}
.topbar .file-tabs li span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  pointer-events: none;
}
.topbar .file-tabs li:hover {
  opacity: 1;
  cursor: pointer;
}
.topbar .file-tabs li .icon {
  margin-left: 5px;
  padding: 5px;
  border-radius: 3px;
}
.topbar .file-tabs li .icon:hover {
  cursor: pointer;
  background: ghostwhite;
}
.topbar .file-tabs li:last-child {
  margin-right: 0;
}
.topbar .file-tabs li.active {
        color: #212121;
        opacity: 1;
        border-bottom: 2px solid #E30712;
}
</style>
