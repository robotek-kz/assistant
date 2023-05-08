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
    allProfileLines: async({commit, dispatch}, id) => {
        const response = await api.get(`/users/episode/${id}/lines`);
        const text = await response.body;
        console.log('episodes', text);
        // console.log('episode2', episodeObject)
        commit(types.SET_PROFILE_APPLICATION_LINES, text);
    },
    generateProfileLine: async({commit, dispatch}, data) => {
        console.log('generateProfileLine', data);
        commit(types.SET_LINE, data);
    },
    finishProfileLine: async ({commit, dispatch}, data) => {
        try {
            const response = await api.put(`/users/lines/${data['id']}/finished`, {
                state: data['state'],
                current_line: data['current_line'],
                current_char: data['current_char'],
                current: data['current'],
            });
        } catch (error) {
            console.log('Ошибка');
        }
    },
    updateProfileLine: async ({commit, dispatch}, data) => {
        try {
            const response = await api.put(`/users/lines/${data['id']}/update`, {
                state: data['state'],
                current_line: data['current_line'],
                current_char: data['current_char'],
                current: data['current'],
            });
        } catch (error) {
            console.log('Ошибка');
        }
    },
    clearProfileLine: async({commit, dispatch}, data) => {
        commit(types.CLEAR_LINE, data)
    }
}