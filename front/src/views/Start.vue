<template>
    <main class="middle">
      <div class="start-block">
        <div class="start-block__info">
          <h1>Добро пожаловать</h1>
          <button @click="refreshLocalStorage">
            <fa :icon="['fas', 'sync-alt']" spin />
          </button>
        </div>
        <div v-if="!isAutheticated" class="buttons">
          <router-link to="/login" class="button">
            <span>Войти</span>
          </router-link>
          <router-link to="/register" class="button">
            <span>Регистрация</span>
          </router-link>
        </div>
      </div>
    </main>
</template>

<script>
import { mapGetters } from 'vuex';

// const api = new ApiService('Something get wrong');
export default {
  name: 'Start',
  data() {
    return {

    };
  },
  computed: {
    ...mapGetters('user', ['isAutheticated']),
  },
  methods: {
    refreshLocalStorage() {
      window.localStorage.removeItem('id_token');
      window.location.reload();
    }
  }
};
</script>

<style lang="sass" scoped>

.start-block
  display: grid
  grid-template-columns: 1fr
  .start-block__info
    display: flex
    justify-content: center
    align-items: center
    border-bottom: 2px solid #E30712
    color: #212121
    padding: 20px
    font-size: 150%
  .start-block__todo
    display: grid
    justify-content: center
    align-items: center

.middle
  display: flex
  flex-direction: column

.ps
  height: 400px



.buttons
  display: flex
  justify-content: center
  align-items: flex-start
  gap: 10px
  margin-top: 2em

.button
  display: flex
  text-align: center
  justify-content: space-around
  color: black
  align-items: center
  background-color: #DCDCDD
  width: 150px
  height: 47px
  border-radius: 3%
  cursor: pointer
  flex-grow: 1
  max-width: 250px

  &:hover
    border: 2px solid #E30712
 



</style>
