import ApiService from "@/services/api.service";
import { types } from "./mutations";
const api = new ApiService('??');

export default {
    all: async({commit, dispatch}, id) => {
        const response = await api.get(`/application/${id}/files`);
        const text = await response.body;
        console.log('files', text)
        const filesObject = text.reduce((result, item) => {
            Object.assign(result, {
                [item.id]: {...item}
            });
            return result;

        }, {});
        commit(types.SET_APPLICATION_FILES, filesObject);
    }
}