<template>
    <div class="application">
        <div class="header">
            <span>
                Программы
            </span>
            <div class="actions">
                <button @click="() => isAdding=true"><fa :icon="['fa', 'plus-circle']" /></button>
            </div>
        </div>
        <div v-if="isAdding" class="upload">
            <div class="form">
                <div class="form-control">
                    <input type="text" v-model="addContent.name">
                </div>
                <div class="form-control">
                    <textarea v-model="addContent.description"></textarea>
                </div>
            </div>
            <div class="form-actions">
                <button @click="() => isAdding=false"><fa :icon="['fas', 'window-close']" size="3x" /></button>
                <button @click="add(addContent); changeAdd()"><fa :icon="['fas', 'thumbs-up']" size="3x" /></button>
            </div> 
        </div>
        <simplebar class="main">
            <div class="box">
                <div v-for="st in getSets">
                    <div v-if="editMode && current === st.id" class="single-update">
                        <div class="form">
                            <div class="form-control">
                                <input type="text" v-model="changeContent.name">
                            </div>
                            <div class="form-control">
                                <textarea name="" id="" cols="30" rows="10" v-model="changeContent.description"></textarea>
                            </div>
                        </div>
                        <div class="form-actions">
                            <button @click="edit(changeContent); changeEdit()"><fa :icon="['fas', 'check']" /></button>
                            <button @click="() => editMode=false"><fa :icon="['fas', 'arrow-circle-left']" /></button>
                        </div>
                    </div>
                    <div v-else class="single">
                        <div class="single-info">
                            <h2>{{  st.name }}</h2>
                            <p>{{  st.description  }}</p>
                            <p>{{ st.user }}</p>
                            <p>{{ st.files }}</p>
                        </div>
                        <div class="single-actions">
                            <button @click="approve(st.id)"><fa :icon="['fas', 'exchange-alt']" /></button>
                            <button @click="prepare(st.id)"><fa :icon="['fas', 'pen']" /></button>
                            <button @click="remove(st.id)"><fa :icon="['fas', 'trash']" /></button>
                            <button @click="showModal(st)"><fa :icon="['fas', 'file']" /></button>
                            <button @click="nextWindow(st.id)"><fa :icon="['fas', 'external-link-square-alt']" /> </button>
                        </div>
                    </div>
                </div>
            </div>
        </simplebar>
        <vue-modal name="my-modal" size="xlg">
            <div v-for="user in users">
                <span><button @click="addToArray(user.id)">{{ user.username }}</button></span>
                <div v-for="app in user.application">
                    <div v-if=" app.application.id === currentApplication.id" style="background-color:green">assign</div>
                </div>
            </div>
            {{ array }}
            <button @click="assign">Assign</button>
        </vue-modal>
        <vue-modal name="file-modal" size="xlg">
            <ApplicationFileUpload :application="currentAppFile"/>
        </vue-modal>
    </div>
</template>


<script>
import { mapActions, mapGetters } from "vuex";
import  ApplicationFileUpload from "@/components/Admin/ApplicationFileUpload.vue";
export default {
    name: "Application",
    data() {
        return {
            editMode: false,
            current: '',
            isAdding: false,
            addContent: {
                name: '',
                description: '',
            },
            changeContent: {
                id: '',
                name: '',
                description: '',
            },
            currentApplication: {},
            currentAppFile: {},
            array: [],
        }
    },
    components: {
        ApplicationFileUpload
    },
    mounted() {
        this.allSet()
    },
    computed: {
        ...mapGetters("sets", ["getSets", "users"]),
    },
    methods: {
        ...mapActions("sets",["allSet", "add", "remove", "edit","allUsers", "assignApplicationToUser"]),
        showModal(app) {
            this.currentAppFile = this.getSets.find(element => element.id === app.id);
            this.$modals.show('file-modal');
        },
        approve(id) {
            this.allUsers();
            this.array = [];
            this.$modals.show('my-modal');
            this.temp_id = id;
                fetch(`http://localhost:5000/api/application/${id}`).then(
                (response) => response.json()
            ).then((body) => this.currentApplication = body);
        },
        addToArray(id) {
            if (this.array.includes(id)) {
                console.log('youu bastard')
            } else {
                this.array.push(id);
            }
        },
        assign() {
            this.assignApplicationToUser({"ids": {"ids": this.array}, "temp_id": this.temp_id});
        },
        prepare(id) {
            this.current = id;
            this.editMode = true;
            const element = this.getSets.find(element => element.id === id);
            this.changeContent.id = element.id;
            this.changeContent.name = element.name;
            this.changeContent.description = element.description;
        },
        changeAdd() {
            this.isAdding = false;
            this.addContent.name = '';
            this.addContent.description = '';
        },
        changeEdit() {
            this.editMode = false;
            this.changeContent.id = '';
            this.changeContent.name = '';
            this.changeContent.description = '';
        },
        nextWindow(id) {
            this.$router.push({name: "Episode", params: {id: id}});
        }
    }
}
</script>

<style scoped>
.application {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 52px auto 1fr;
}

.application .header {
  color: #212121;
  border-bottom: 2px solid #E30712;
  padding: 0.5em;
  font-size: 150%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.application .header .actions button:hover {
    color: #133D52;
    font-size: 1.1em;
}

.application .upload {
    margin: 2em;
    box-sizing: border-box;
    font-size: 12px;
    resize: none;
    display: flex;
    justify-content: center;
}

.application .upload .form {
    border-left: 2px solid #ccc;
    background-color: #f8f8f8;
    width: 50%;
}
.application .upload .form-actions {
    padding: 1.2em;
    background-color: #f8f8f8;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
}

.application .upload .form .form-control {
    display: block;
    padding: 1.5em;
}
.application .upload .form .form-control input {
    border: 2px solid #ccc;
    border-radius: 5px;
    font-size: 2em;
}
.application .upload .form .form-control textarea {
    border: 2px solid #ccc;
    border-radius: 5px;
    width: 100%;
    height: 100%;
    resize: none;
}
.application .upload .form-actions button:hover {
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
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.main .box .single .single-actions {
    display: flex;
    gap: 0.5em;
}
.main .box .single .single-actions button:hover {
    color: #133D52;
    font-size: 1.1em;
}
.main .box .single-update {
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
.main .box .single-update .form .form-control textarea {
    border: 2px solid #ccc;
    border-radius: 5px;
    width: 100%;
    height: 100%;
    resize: none;
}
.main .box .single-update .form-actions button:hover {
    color: #133D52;
    font-size: 1.1em;
}
</style>