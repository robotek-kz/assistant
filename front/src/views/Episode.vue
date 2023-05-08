<template>
    <div class="episode">
        <div class="header">
            <span>
                {{  getSet.name }}
            </span>
            <div class="actions">
                <button @click="() => isAdding=true"><fa :icon="['fa', 'plus-circle']" /></button>
            </div>
        </div>
        <div v-if="isAdding" class="upload">
            <div class="form">
                <div class="form-control">
                    <input type="text" v-model="addEpisode.name">
                </div>
            </div>
            <div class="form-actions">
                <button @click="() => isAdding=false"><fa :icon="['fas', 'window-close']" size="3x" /></button>
                <button @click="add(addEpisode); changeAdd()"><fa :icon="['fas', 'thumbs-up']" size="3x" /></button>
            </div> 
        </div>
        <simplebar class="main">
            <div class="box">

                {{ getEpisodes  }}
                <div v-for="episode, index in getEpisodes" :key="episode.id">
                    <div v-if="editMode && current === episode.id" class="single-update">
                        <div class="form">
                            <div class="form-control">
                                <input type="text" v-model="changeEpisode.name">
                            </div>
                        </div>
                        <div class="form-actions">
                            <button @click="edit(changeEpisode); changeEdit()"><fa :icon="['fas', 'check']" /></button>
                            <button @click="() => editMode=false"><fa :icon="['fas', 'arrow-circle-left']" /></button>
                        </div>
                    </div>
                    <div v-else class="single">
                        <div class="single-info">
                            <h2>{{ episode.name  }}</h2>
                            <div v-for="file in episode.files" style="float:left">
                                {{  file.name }}
                            </div>
                            <div v-for="line in episode.lines" style="float:left">
                                {{  line.name }}
                            </div>
                            <!-- <FileComponent :url="episode.files_url"></FileComponent> -->
                        </div>
                        <div class="single-actions">
                            <button @click="prepare(episode.id)"><fa :icon="['fas', 'pen']" /></button>
                            <button @click="remove(episode.id)"><fa :icon="['fas', 'trash']" /></button>
                            <button @click="showModal(episode.id)"><fa :icon="['fas', 'file']" /></button>
                            <button @click="openLinesEditor(episode.id)"><fa :icon="['fas', 'external-link-square-alt']" /></button>
                        </div>
                    </div>
                </div>
            </div>
        </simplebar>
        <vue-modal name="my-modal" size="xlg">
            <MultiFileUpload :set="getSet" :episode="currentEpisode"/>
        </vue-modal>
        <component
        :is="componentType">
        </component>
    </div>
</template>


<script>
import { mapGetters, mapActions } from 'vuex';
import FilesUpload from '@/components/Admin/FilesUpload.vue'
import MultiFileUpload from '@/components/Admin/MultiFileUpload.vue';
// import FileComponent from '../components/FileComponent.vue';
import { 
    PlusCircleIcon } from "vue-feather-icons";
export default {
    name: "Episode",
    data() {
        return {
            componentType: '',
            currentSet: {},
            currentEpisode: {},
            editMode: false,
            current: '',
            isAdding: false,
            addEpisode: {
                application_id: this.$route.params.id,
                name: ''
            },
            changeEpisode: {
                id: '',
                name: '',
            }
        }
    },
    components: {
        FilesUpload,
        MultiFileUpload,
        PlusCircleIcon,
    },
    computed: {
        ...mapGetters("episodes", ["getEpisodes"]),
        ...mapGetters("sets", ["getSets"]),
        getSet() {
            return this.getSets.find(element => element.id === Number(this.$route.params.id));
        },
        loadFiles(url) {
            const result = fetch(`http://localhost:5000/${url}`)
            return result
        }
    },
    mounted() {
        this.allSet();
        const id = this.$route.params.id;
        this.all(id);
    },
    methods: {
        ...mapActions("sets", ["allSet"]),
        ...mapActions("episodes", ["all", "add", "edit", "remove"]),
        ...mapActions("lines_editor", ["setCurrentLinesEditor"]),
        changeComponent(type) {
            this.componentType = type; 
        },
        prepare(id) {
            this.current = id;
            this.editMode = true;
            const element = this.getEpisodes.find(element => element.id === id);
            this.changeEpisode.id = element.id;
            this.changeEpisode.name = element.name;      
        },
        changeAdd() {
            this.isAdding = false;
            this.addEpisode.name = '';
        },
        changeEdit() {
            this.editMode = false;
            this.changeEpisode.id = '';
            this.changeEpisode.name = '';
        },
        showModal(id) {
            this.currentEpisode = this.getEpisodes.find(element => element.id === id);
            this.$modals.show('my-modal');
        },
        openLinesEditor(id) {
            const episode = this.getEpisodes.find(episode => episode.id === id)
            this.setCurrentLinesEditor(episode);
            this.$router.push('/lines-editor');
        },
    }
}
</script>

<style scoped>
.episode {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 52px auto 1fr;
}
.episode .header {
  color: #212121;
  border-bottom: 2px solid #E30712;
  padding: 0.5em;
  font-size: 150%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.episode .header .actions button:hover {
    color: #133D52;
    font-size: 1.1em;
}

.episode .upload {
    margin: 2em;
    box-sizing: border-box;
    font-size: 12px;
    resize: none;
    display: flex;
    justify-content: center;
}


.episode .upload .form {
    border-left: 2px solid #ccc;
    background-color: #f8f8f8;
    width: 50%;
}
.episode .upload .form-actions {
    padding: 1.2em;
    background-color: #f8f8f8;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
}

.episode .upload .form .form-control {
    display: block;
    padding: 1.5em;
}
.episode .upload .form .form-control input {
    border: 2px solid #ccc;
    border-radius: 5px;
    font-size: 2em;
}
.episode .upload .form-actions button:hover {
    color: #133D52;
    font-size: 1.1em;
}
.main {
    height: 100vh;
}
.main .box {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1em;
    padding: 2em;
}
.main .box .single {
    height: 100px;
    display: flex;
    flex-direction: row;
    justify-content: space-between; 
}
.main .box .single .single-actions {
    display: flex;
    align-items: flex-start;
    gap: 0.5em;
}
.main .box .single .single-actions button:hover {
    color: #133D52;
    font-size: 1.1em;
}

.main .box .single-update {
    height: 100px;
    box-sizing: border-box;
    resize: none;
    display: flex;
    justify-content: center;
}

.main .box .single-update .form {
    padding: 0.5em;
    background-color: #f8f8f8;
}
.main .box .single-update .form-actions {
    padding: 0.5em;
    background-color: #f8f8f8;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
}
.main .box .single-update .form .form-control input {
    border: 2px solid #ccc;
    border-radius: 5px;
    font-size: 1.5em;
    margin-bottom: 0.2em;
}
.main .box .single-update .form-actions button:hover {
    color: #133D52;
    font-size: 1.1em;
}
</style>