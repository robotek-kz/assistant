<template>
    <div class="game-explorer">
        <simplebar class="content-area">
                <GameListing
                    :gameFiles="gameFiles"
                />
        </simplebar>
    </div>
</template>


<script>
import { mapGetters } from "vuex";
import GameListing from '@/components/GameSketch/GameListing.vue';
export default {
    name: "GameExplorer",
    components: {
        GameListing,
    },
    data() {
        return {
        }
    },
    props: {
        gameFiles: Array,
    },
    computed: {
    },
    methods: {
    },
    mounted() {
    }
}

</script>


<style scoped>
.simplebar-scrollbar {
    background-color: #DCDCDD;
}
.game-explorer {
    background: #F3F3F3;
    z-index: 9;
    border-right: 2px solid #E30712;
    display: flex;
    flex-direction: column;
    height: 100vh;
    min-width: 0;
    min-height: 0;
}

.game-explorer header {
    display: flex;
    flex-direction: row;
    padding: 5px 10px 5px 10px;
    align-items: center;
    z-index: 99;
}

.game-explorer header h4 {
    color: #212121;
    font-weight: bold;
    flex: 1;
}

.game-explorer header .menu {
    display: flex;
}

.game-explorer header .menu .icon-wrapper {
    position: relative;
}

.game-explorer header .menu .icon-wrapper .tooltip {
    position: absolute;
    background: ghostwhite;
    top: 35px;
    left: -100px;
}
.content-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: auto;
}

</style>