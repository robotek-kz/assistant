<template>
    <div class="register-block">
      <h1>Войдите в аккаунт</h1>
      <ul v-if="errors" class="error-messages">
        <li v-for="(v, k) in errors" :key="k">
          {{ v }}
        </li>
      </ul>
      <div class="register-nickname">
        <input
          id="nickname"
          v-model.trim="user.nickname"
          type="text"
          required
        >
        <label for="nickname" class="title">Никнейм</label>
      </div>
      <div class="register-password">
        <input
          id="password"
          v-model.trim="user.password"
          type="password"
          required
        >
        <label for="password" class="title">Пароль</label>
      </div>
      <router-link to="/register">
        Нету аккаунта?
      </router-link>
      <button class="button" @click="onSubmit">
        <span v-if="!isLoading">Войти</span>
        <fa v-if="isLoading" :icon="['fas', 'spinner']" spin />
      </button>
    </div>
</template>


<script>

import { mapState } from 'vuex';
export default {
  name: 'Login',
  data() {
    return {
      user: {
        nickname: '',
        password: '',
      },
      isLoading: false,
    };
  },
  computed: {
    ...mapState('user', {
      errors: (state) => state.errors,
    }),
  },
  methods: {
    onSubmit() {
      this.isLoading = true;
      const temp = this.$store.dispatch('user/login', {
        nickname: this.user.nickname,
        password: this.user.password,
      });
      temp.then((data) => {
        if (data === false) {
          this.isLoading = false;
        } else {
          this.isLoading = false;
          this.$store.commit('user/setError', null);
          this.$router.push({ name: 'nickname', params: { nickname: this.user.nickname } });
          this.user.nickname = '';
          this.user.password = '';
        }
      });
    },
  },
};

</script>



<style lang="sass" scoped>

.register-block
  display: flex
  flex-direction: column
  align-items: center
  justify-content: center
  margin-bottom: 10em

  .register-name
    display: flex
    flex-direction: column

  .register-nickname
    display: flex
    flex-direction: column

  .register-password
    display: flex
    flex-direction: column

  div
    padding: 1.3em

.title
  padding: 0.65rem 0.5rem
  position: absolute
  transition: 1s
  color: #212121


input
  border-bottom: 2px solid #E30712
  background: #DCDCDD
  padding: 0.7em
  border-radius: 3%

  &:focus ~ .title
    transform: translateY(-2.2rem) scale(0.8)
  &:valid ~ .title
    transform: translateY(-2.2rem) scale(0.8)


.error-messages
  li
    list-style-type: none
    font-size: 1.3em
    padding-bottom: 0.5em


.button
  display: flex
  text-align: center
  justify-content: space-around
  align-items: center
  width: 200px
  height: 40px
  background: #DCDCDD
  margin-top: 5px
  cursor: pointer
  border-radius: 5px

  &:hover
    border: 2px solid #E30712

</style>
