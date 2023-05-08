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
        const response = await api.get(`/application/${id}/episodes`);
        const text = await response.body;
        console.log('episodes', text);
        const episodeObject = text.reduce((result, item) => {
            Object.assign(result, {
                [item.id]: {...item}
            });
            return result;

        }, {});
        // console.log('episode2', episodeObject)
        commit(types.SET_EPISODES, text);
    },
    add: async({commit, dispatch}, data) => {    
        const response = await api.post(`/application/${data.application_id}/episode`, {
            name: data.name,
            path: data.name,
        });
        const text = await response.body;
        console.log('text', text);
        commit(types.NEW_EPISODE, text);
        // dispatch("all");
    },
    remove: async({commit, dispatch}, id) => {
        const response = await api.delete(`/episode/${id}`);
        const text = await response.body;
        commit(types.REMOVE_EPISODES, id);
    },
    edit: async({commit, dispatch}, content) => {
        console.log('content:', content.description);
        const response = await api.put(`/episode/${content.id}`, {
            name: content.name,
            path: content.name,
        })
        const text = await response.body;
        commit(types.UPDATE_EPISODES, text);
    },
    addFile: async ({commit, dispatch},data) => {
        const response = await api.upload(`/episode/${data.episode.id}/files`,data.formData, data.episode);
        const text = await response.body;
        const upd = {'episode': data.episode, 'files': text}
        commit(types.ADD_FILE, upd);
    }
}