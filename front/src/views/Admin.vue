<template>
    <div class="admin">
        <div class="header">
            Панель администратора
        </div>
        <div class="main">
            <div class="box users">
                <div class="head-info">
                    <span>
                        Пользователи
                    </span>
                    <fa :icon="['fas', 'external-link-square-alt']" /> 
                </div>
                <div class="body-info">
                    body
                </div>
            </div>
            <div class="box presentations">
                <div class="head-info">
                    <span>
                        Презентации
                    </span>
                    <fa :icon="['fas', 'external-link-square-alt']" /> 
                </div>
                <div class="body-info">
                    body
                </div>
            </div>
            <div class="box lessons">
                <div class="head-info">
                    <span>
                        Уроки
                    </span>
                    <fa :icon="['fas', 'external-link-square-alt']" /> 
                </div>
                <div class="body-info">
                    body
                </div>
            </div>
            <div class="box applications">
                <div class="head-info">
                    <span>
                        Программы
                    </span>
                    <router-link to="/application">
                        <fa :icon="['fas', 'external-link-square-alt']" /> 
                    </router-link>
                </div>
                <div class="body-info">
                    body
                </div>  
            </div> 
        </div>
    </div>
</template>


<script>
import { mapActions, mapGetters } from "vuex";
export default {
    name: "Admin",
    data() {
        return {
        }
    },
    mounted() {
        this.all()
    },
    computed: {
        ...mapGetters("sets", ["getSets"])
    },
    methods: {
        ...mapActions("sets",["all", "add", "remove", "edit"]),
    }
}
</script>

<style scoped>
.admin {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 52px 1fr;
}

.admin .header {
  color: #212121;
  border-bottom: 2px solid #E30712;
  padding: 0.5em;
  font-size: 150%;
}

.main {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-areas: 
        "users applications"
        "lessons presentations";
    padding: 2em;
    gap: 2em;
}

.main .box {
  background-color: #DCDCDD;
  color: #212121;
  border-radius: 5px;
  padding: 20px;
  font-size: 150%;
}
.main .box .head-info {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.main .users {
    grid-area: users;
}
.main .presentations {
    grid-area: presentations;
}
.main .lessons {
    grid-area: lessons;
}
.main .applications {
    grid-area: applications;
}

.fa-external-link-square-alt:hover {
    color: #133D52;
    font-size: 1.1em;
}
</style>