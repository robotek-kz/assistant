<template>
<div class="uploadBox">
    <h3>{{ headerMessage }}</h3>
    <form role="form" enctype="multipart/form-data" @submit.prevent="onSubmit">
        <div class="uploadBoxMain" v-if="!itemsAdded">
            <div class="form-grou">
                <div class="dropArea" @ondragover="onChange" :class="dragging ? 'dropAreaDragging' : ''" @dragenter="dragging=true" @dragend="dragging=false" @dragleave="dragging=false">
                    <h3>{{ dropAreaPrimaryMessaage }}</h3>
                    <input type="file" id="items" name="items[]" requred multiple @change="onChange"/>
                    <p class="help-block">{{ dropAreaSecondaryMessage }}</p>
                </div>
            </div>
        </div>
        <div v-else class="uploadBoxMain">
            <p><strong>{{ fileNameMessage }}</strong></p>
            <ol>
                <li v-for="name in itemsNames">{{ name }}</li>
            </ol>
            <p><strong>{{  fileSizeMessage }}</strong></p>
            <ol>
                <li v-for="size in itemsSizes">{{  size }}</li>
            </ol>
            <p><strong>{{ totalFileMessage }}</strong>{{  itemsAdded }}</p>
            <p><strong>{{ totalUploadSizeMessage }}</strong>{{ itemsTotalSize }}</p>
            <button class="btn" @click="removeItems">{{  removeFileMessage }}</button>
            <div class="loader" v-if="isLoaderVisible">
                <div class="loaderImg"></div>
            </div>
        </div>
        <div class="upload-actions">
            <button type="submit" class="btn" :disabled="itemsAdded < minItems || itemsAdded > maxItems">
                {{ uploadButtonMessage }}
            </button>
            <button type="button" class="btn" @click="removeItems">{{  cancelButtonMessage }}</button>
        </div>
        <br>
        <div class="successMsg" v-if="successMsg !== ''">{{ successMsg }}</div> 
    </form>
</div>

</template>

<script>
import ApiService from '@/services/api.service';
import { mapGetters, mapActions } from 'vuex';
const api = new ApiService('??')
export default {
    name: "MultiFileUpload",
    data() {
        return {
            headerMessage: "Добавьте файлы для загрузки",
            dropAreaPrimaryMessaage: "Перекиньте файлы",
            dropAreaSecondaryMessage: "Файлы с расширениями py, js, html, c, v",
            dragging: false,
            itemsAdded: '',
            fileNameMessage: "Имя файла:",
            fileSizeMessage: "Размер:",
            itemsNames: [],
            itemsSizes: [],
            itemsAdded: '',
            removeFileMessage: "Удалить файлы",
            totalFileMessage: "app.py",
            totalUploadSizeMessage: "30kB",
            isLoaderVisible: false,
            maxItems: 20,
            minItems: 1,
            cancelButtonMessage: 'Отмена',
            uploadButtonMessage: 'Загрузить',
            successMsg: 'Файлы загружены'
        }
    },
    props: {
        set: {},
        episode: {},
    },
    computed: {
        ...mapGetters("episode_files", ["getEpisodeFiles"])
    },
    mounted() {
        console.log('hello', this.episode);
        this.all(this.episode.id);
    },
    methods: {
        ...mapActions("episode_files", ["all"]),
        ...mapActions("episodes", ["addFile"]),
        onChange(e) {

            this.successMsg = '',
            this.formData = new FormData();
            let files = e.target.files || e.dataTransfer.files;
            this.itemsAdded = files.length;
            let fileSizes = 0;
            console.log(this.itemsAdded);
            console.log('files:', files);
            for (let x in files) {
                if (!isNaN(x)) {
                    this.items = e.target.files[x] || e.dataTransfer.files[x];
                    console.log(files[x].name);
                    this.itemsNames[x] = files[x].name;
                    this.itemsSizes[x] = files[x].size;
                    fileSizes += files[x].size;
                    console.log(this.episode);
                    this.formData.append('py', this.items);
                    // console.log(this.formData);
                 }
            }
            this.itemsTotalSize = this.fileSizes;
            // console.log('thisFormData', this.formData.items);
        },
        removeItems() {
            this.items = '',
            this.itemsAdded = '',
            this.itemsNames = [],
            this.itemsSizes = [],
            this.itemsTotalSize = ''
            this.dragging = false
        },
        onSubmit() {
            // console.log('this.sets', this.set);
            // console.log('this.episode', this.episode);
            this.isLoaderVisible = true;
            // api.upload('files', this.formData, this.episode);
            const data = {'formData':this.formData, 'episode': this.episode};

            this.addFile(data);
            this.isLoaderVisible = false;
            this.removeItems();
        }
    }
}

</script>


<style scoped>
.uploadBox {
    position: relative;
    background: #eee;
    padding: 0 1em 1em 1em;
    margin: 1em;
}

.uploadBox h3 {
    padding-top: 1em;
}

.uploadBox .uploadBoxMain {
    position: relative;
    margin-bottom: 1em;
    margin-right: 1em;
}

.uploadBox .dropArea {
    position: relative;
    width: 100%;
    height: 300px;
    border: 5px dashed #00ADCE;
    text-align: center;
    font-size: 2em;
    padding-top: 80px;
}

.uploadBox .dropArea input {
    position: absolute;
    cursor: pointer;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
}

.uploadBox .loader {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #fff;
    opacity: 0.9;
}

.upload-actions {
    display: flex;
    flex-direction: row;
    gap: 2em;
}

.uploadBoxMain {
    padding: 2em;
}
.btn {
  display: flex;
  text-align: center;
  justify-content: space-around;
  align-items: center;
  width: 200px;
  height: 40px;
  background: #DCDCDD;
  margin-top: 5px;
  cursor: pointer;
  border-radius: 5px;
}
.btn:hover {
    border: 2px solid #E30712;
}
</style>