import ApiService from "@/services/api.service";
import { types } from "./mutations";
const api = new ApiService('??');
class Sets {
    constructor({ id, name, description }) {
        this.id = id;
        this.name = name;
        this.description = description;
    }
}
export default {
    allUsers: async({commit, dispatch}) => {
        const response = await api.get('/users');
        console.log('user.response', response);
        const data = await response.body;
        console.log('users', data);
        commit(types.SET_ALL_USER, data);
    },
    assignApplicationToUser: async({commit, dispatch}, ids) => {
        console.log('ids', ids);
        const response = await api.post(`/application/${ids.temp_id}/create`, ids.ids)
        const data = await response.body;
        commit(types.SET_ALL_USER, data);
        dispatch("allSet");
    },
    allSet: async({commit, dispatch}) => {
        const response = await api.get('/application');
        const text = await response.body;
        const setsObject = text.reduce((result, item) => {
            Object.assign(result, {
                [item.id]: new Sets({...item})
            });
            return result;

        }, {});
        commit(types.SET_SETS, text);
    },
    add: async({commit, dispatch}, data) => {        
        const response = await api.post('/application', {
            name: data.name,
            description: data.description,
            path: data.name,
        });
        const text = await response.body;
        commit(types.NEW_SET, text)
    },
    remove: async({commit, dispatch}, id) => {
        const response = await api.delete(`/application/${id}`);
        const text = await response.body;
        commit(types.REMOVE_SETS, id);
        // dispatch("all");
    },
    edit: async({commit, dispatch}, content) => {
        console.log('content:', content.description);
        const response = await api.put(`/application/${content.id}`, {
            name: content.name,
            description: content.description,
            path: content.name,
        })
        const text = await response.body;
    },
    addFile: async({commit, dispatch}, data) => {
        const response = await api.upload(`/application/${data.application.id}/files`,data.formData, data.application);
        const text = await response.body;
        const upd = {'application': data.application, 'files': text}
        commit(types.ADD_FILE, upd);
    }
}