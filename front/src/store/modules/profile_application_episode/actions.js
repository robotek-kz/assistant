import ApiService from "@/services/api.service";
import { types } from "./mutations";
const api = new ApiService('??');
class Episode {
    constructor({ id, name, application_id }) {
        this.id = id;
        this.name = name;
        this.application_id = application_id;
    }
}
export default {
    all: async({commit, dispatch}, id) => {
        const response = await api.get(`/users/application/${id}/episodes`);
        const text = await response.body;
        console.log('episodes', text);
        // console.log('episode2', episodeObject)
        commit(types.SET_PROFILE_APPLICATION_EPISODES, text);
    },
    clear: async({commit,dispatch}, id) => {
        commit(types.CLEAR_PROFILE_APPLICATION_EPISODES);
    }
}