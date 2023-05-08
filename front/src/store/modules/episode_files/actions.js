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
        const response = await api.get(`/episode/${id}/files`);
        const text = await response.body;
        console.log('files', text)
        const filesObject = text.reduce((result, item) => {
            Object.assign(result, {
                [item.id]: {...item}
            });
            return result;

        }, {});
        console.log('files2', filesObject)
        commit(types.SET_EPISODE_FILES, filesObject);
    },
    add: async({commit, dispatch}, data) => {        
        const response = await api.post('/application', {
            name: data.name,
            description: data.description
        });
        const text = await response.body;
        dispatch("all");
    },
    remove: async({commit, dispatch}, id) => {
        const response = await api.delete(`/application/${id}`);
        const text = await response.body;
        dispatch("all");
    },
    edit: async({commit, dispatch}, content) => {
        console.log('content:', content.description);
        const response = await api.put(`/application/${content.id}`, {
            name: content.name,
            description: content.description,
        })
        const text = await response.body;
        dispatch("all");
    }
}