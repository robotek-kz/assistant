<template>
    <div class="game-listing">
        <div class="header">
            <span>['Скетчи']</span>
            <button @click="back">Назад</button>
        </div>
        <GameItem
            v-for="(game, index) in gameFiles"
            :key="index"
            :gameItem="game"
        />
    </div>
</template>


<script>
    
import GameItem from "@/components/GameSketch/GameItem.vue";
import { mapGetters } from "vuex";
export default {
    props: {
        gameFiles: Array
    },
    components: {
        GameItem
    },
    mounted() {
        console.log('from gamelisting', this.gameFiles);
        this.gameFiles;
    },
    computed: {
        ...mapGetters("user", ["currentUser"])
    },
    methods: {
        back() {
            this.$router.push({name: 'nickname',params: {nickname: this.currentUser.nickname}})
        }
    }
}
</script>



<style>
.header {
  color: #212121;
  border-bottom: 2px solid #E30712;
  padding: 0.45em;
  font-size: 150%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

</style>