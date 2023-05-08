import ApiService from "@/services/api.service";
import { types } from "./mutations";

const api = new ApiService('Я обещаю починить это');
export default {
    allLoad: async({state, commit}, id) => {
        if (!state.projects.length) {
            try {
                const response = await api.get(`/users/${id}/project_game_sketches`);
                const body = await response.body;
                commit(types.SET_PROJECTS, body.data);
            } catch (error) {
                console.log('Ошибка', error);
            }
        }
    },
    generateSketch: ({state, commit}, item) => {
        console.log('helloman');
        commit(types.SET_GAME_SKETCH, item);
    },
    updateFileSketch: async ({commit}, data) => {
        console.log('updatefilsketch', data);
        try {
            commit(types.UPDATE_FILE_GAME_SKETCH, data);
            const response = await api.put(`/file_game_sketches/${data['id']}`, {
                code: data['ready'],
                previous_code: data['previous_ready']
            });
        } catch (error) {
            console.log('Ошибка',error);
        }
    },
    updateGameSketch: async ({commit}, data) => {
        try {
            console.log('hello data', data);
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
    resetGameSketch: ({commit}) => {
        commit(types.SET_GAME_SKETCH, {});
    },
    resetState: ({commit}) => {
        commit(types.RESET_MODULE_STATE);
    }
}