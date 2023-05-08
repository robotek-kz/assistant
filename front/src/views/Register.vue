<template>
    <div class="register-block">
      <h1>Регистрация нового пользователя</h1>
      <ul v-if="errors" class="error-messages">
        <li v-for="(v, k) in errors" :key="k">
          {{ v }}
        </li>
      </ul>
      <div class="register-name">
        <input
          id="name"
          v-model.trim="user.username"
          type="text"
          required
        >
        <label for="name" class="title">Имя пользователя</label>
      </div>
      <div class="register-nickname">
        <input
          id="nickname"
          v-model.trim="user.nickname"
          type="text"
          required
        >
        <label for="nickname" class="title">Придумайте ник</label>
      </div>
      <div class="register-password">
        <input
          id="password"
          v-model.trim="user.password"
          type="password"
          required
        >
        <label for="password" class="title">Придумайте пароль</label>
      </div>
      <router-link to="/login">
        Есть аккаунт?
      </router-link>
      <button class="button" @click="onSubmit">
        <span v-if="!isLoading">Создать</span>
        <fa v-if="isLoading" :icon="['fas', 'spinner']" spin />
      </button>
    </div>
</template>


<script>

import { mapState } from 'vuex';

export default {
  name: 'Register',
  data() {
    return {
      user: {
        username: '',
        nickname: '',
        password: '',
      },
      isLoading: false,
    };
  },
  computed: {
    ...mapState({
      errors: (state) => state.errors,
    }),
  },
  methods: {
    onSubmit() {
      this.isLoading = true;
      const temp = this.$store.dispatch('user/register', {
        username: this.user.username,
        nickname: this.user.nickname,
        password: this.user.password,
      });
      temp.then((data) => {
        if (data === false) {
          this.isLoading = false;
        } else {
          this.isLoading = false;
          this.$store.commit('setError', null);
          this.$router.push('/login');
          this.user.username = '';
          this.user.nickname = '';
          this.user.password = '';
        }
      });
      // if (!isEmpty) {
      //   this.isLoading = false;
      //   this.$router.push('/');
      // } else {
      //   this.isLoading = false;
      // }
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
  border-bottom: 1px solid #E30712
  padding: 0.7em
  background: #DCDCDD
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
