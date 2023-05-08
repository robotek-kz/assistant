<template>
    <div :class="['file-item', { active: isActive }]">
    <div
        class="clickable-area"
        @click="openFile({ file_id: file.file_id })"
        @dblclick="readonly = !readonly">
        <FileTextIcon class="icon" size="18" />
        <form @submit.prevent="$refs.input.blur()">
            <input 
            :ref="'input'"
            type="text"
            v-model="filename"
            :readonly="readonly"
            size="2"
            @blur="changeFileName">
        </form>
    </div>
        <div class="context-menu">
            <MoreVerticalIcon
                class="trigger-icon"
                size="18"
                @click="toggleContextMenu"
            />
            <SlideYUpTransition>
                <div v-if="showContextMenu" class="options" v-click-outside="toggleContextMenu">
                    <div class="option-item" @click="openRenameMode">
                        <edit3-icon size="18" class="icon" />Переименовать
                    </div>
                    <div class="option-item">
                        <download-icon size="18" class="icon" />Скачать
                    </div>
                    <div class="option-item">
                        <copy-icon size="18" class="icon" />Клонировать
                    </div>
                    <div class="option-item">
                        <copy-icon size="18" class="icon" />Скопировать
                    </div>
                    <div class="option-item" @click="deleteCurrentFile">
                        <trash2-icon size="18" class="icon" />Удалить
                    </div>
                </div>
            </SlideYUpTransition>
        </div>
    </div>
</template>


<script>
import { 
    FileTextIcon,
    MoreVerticalIcon,
    Trash2Icon,
    Edit3Icon,
    DownloadIcon,
    CopyIcon,
    ClipboardIcon } from "vue-feather-icons";
import { mapActions } from "vuex";
import { SlideYUpTransition } from "vue2-transitions";
export default {
    components: {
        FileTextIcon,
        MoreVerticalIcon,
        Trash2Icon,
        Edit3Icon,
        DownloadIcon,
        CopyIcon,
        ClipboardIcon,
        SlideYUpTransition
    },
    data() {
        return {
            readonly: true,
            filename: "",
            showContextMenu: false,
        };
    },
    props: {
        file: Object,
        isActive: Boolean
    },
    methods: {
        ...mapActions("editor", ["openFile"]),
        ...mapActions("files", ["renameFile", "deleteFile"]),
        changeFileName() {
            console.log('chanage file name');
            if (this.filename) {
                this.renameFile({ file_id: this.file.file_id, name: this.filename});
                this.readonly = true;
                this.openFile({ file_id: this.file.file_id });
            } else {
                this.deleteFile({ file_id: this.file.file_id });
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
        deleteCurrentFile() {
            this.showContextMenu = !this.showContextMenu;
            this.deleteFile({ file_id: this.file.file_id });
        }
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
};
</script>



<style>
.file-item {
    display: flex;
    color: #E30712;
    flex-direction: row;
    align-items: center;
    padding: 2px 5px 2px 0;
    margin: 2px 5px;
    border-radius: 5px;
}

.file-item .clickable-area {
    display: flex;
    align-items: center;
    flex: 1;
    padding: 3px 10px;
}

.file-item.active {
    background: #FFCDD2;
}
.file-item .icon {
    margin-right: 10px;
}

.file-item:hover {
    background: ghostwhite;
    cursor: pointer;
}

.file-item:hover .context-menu {
    display: flex;
}

.file-item:hover .context-menu .trigger-icon {
    visibility: visible;
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
    color: black;
    padding: 5px;
    border-radius: 5px;
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
    background-color: ghostwhite;
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
</style>