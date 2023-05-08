import ApiService from "@/services/api.service";
import { types } from "./mutations";
const api = new ApiService('??');
export default {
    setCurrentLinesEditor: async({commit, dispatch}, data) => {
        console.log('data', data);
        const response = await api.get(`/episode/${data.id}/files`);
        const text = await response.body;
        const filesObject = text.reduce((result, item) => {
            Object.assign(result, {
                [item.id]: {...item}
            });
            return result;

        }, {});
        console.log('lines_EDITOR', filesObject);
        commit(types.SET_LINES_EDITOR, filesObject);
        commit(types.SET_CURRENT_EPISODE, data.id);
    }
}