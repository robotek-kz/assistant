import Vue from 'vue';
import Vuex from 'vuex';

import modules from "./modules";
Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    ...modules,
  },
  state: {

  },
  actions: {
      clearAll({commit, dispatch}) {
          Object.keys(modules).forEach((moduleName) => {
              try {
                  commit(`${moduleName}/reset`);
              } catch (error) {
                  if (process.env.VUE_APP_ENV === "dev") {
                      console.log(
                          "NO RESET MUTATION FOUND",
                      )
                  }
              }
          });
          dispatch("clearCore");
      }
  },
  mutations: {},
});
